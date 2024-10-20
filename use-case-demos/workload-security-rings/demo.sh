#!/bin/bash

set -e # make sure the job fails if any instruction fails

declare -a SECURITY_RINGS=("sensitive" "unhardened")

function label_nodes {
    nodes=$1
    num=$2

    for node in "${nodes[@]}"
    do
        kubectl label nodes ${node} security-ring=${SECURITY_RINGS[${RANDOM} % ${num}]} --overwrite
    done
}

function deploy {
    echo -e "\n[*] Deploy $1"
    kubectl apply -f "$1"

    if [ ${kind} != "pod" ]; then
        sleep 1 # wait for all pods to show up
    fi

    echo -e "\n[+] Pod's node selector"
    if [ ${kind} == "pod" ]; then
        kubectl get -f "$1" -o json | jq -r '.items[] | "\(.metadata.name) name -> \(.spec.nodeSelector)"'
    else
        kubectl get pods -o json | jq -r '.items[] | "\(.metadata.name) name -> \(.spec.nodeSelector)"'
    fi

    echo -e '\nWaiting for the deployment...'
    if [ ${kind} == "pod" ]; then
        kubectl wait -f "$1" --for=condition=Ready
    else
        kubectl rollout status -f "$1"
    fi

    echo -e '\n[+] Pod schedules'
    kubectl get pods -o wide

    echo -e '\n[+] Delete pod'
    kubectl delete -f "$1"
}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# minikube start --nodes=8

kind="${1:-pod}"

if [ ${kind} != "pod" ] && [ ${kind} != "deployment" ]
then
    echo 'Invalid argument value. Valid argument values are: pod (default), deployment'
    exit 1
fi

echo '[*] Nodes'
kubectl get nodes

echo -e '\n[*] Set node labels'
control_plane_nodes=$(kubectl get nodes -l node-role.kubernetes.io/control-plane -o json | jq -r '.items[].metadata.name')
readarray -t control_plane_nodes <<< "${control_plane_nodes}"
label_nodes ${control_plane_nodes} 1
nodes=$(kubectl get nodes -l !node-role.kubernetes.io/control-plane -o json | jq -r '.items[].metadata.name')
readarray -t nodes <<< "${nodes}"
label_nodes ${nodes} 2

echo -e '\n[*] Node labels'
kubectl get nodes --show-labels

echo -e '\n[*] Install admission control service'
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-audit
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager

echo -e '\n[*] Allow Gatekeeper to reject workloads that create pods violating constraints'
kubectl create -f "${SCRIPT_DIR}/policy/expansion-template.yaml"

echo -e '\n[*] Use Gatekeeper to mutate the node selector config'
kubectl create -f "${SCRIPT_DIR}/policy/mutation.yaml"

echo -e '\n[*] Use Gatekeeper to validate the node selector config'
echo -e '[+] Add constraint template'
kubectl create -f "${SCRIPT_DIR}/policy/allowed-nodeselector-values-template.yaml"
kubectl create -f "${SCRIPT_DIR}/policy/template.yaml"
echo -e '[+] Add constraint'
kubectl create -f "${SCRIPT_DIR}/policy/allowed-nodeselector-values-constraint.yaml"
kubectl create -f "${SCRIPT_DIR}/policy/constraint.yaml"

if [ ${kind} == "pod" ]; then
    deploy "${SCRIPT_DIR}/resources/pods.yaml"
else
    deploy "${SCRIPT_DIR}/resources/deployments.yaml"
fi

# # Wait for manual interaction with the example application
# echo ''
# read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Delete Gatekeeper resources'
kubectl delete -f "${SCRIPT_DIR}/policy/allowed-nodeselector-values-constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/allowed-nodeselector-values-template.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/template.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/mutation.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/expansion-template.yaml"

echo -e '\n[*] Uninstall admission control service'
helm delete gatekeeper --namespace gatekeeper-system
kubectl delete crd -l gatekeeper.sh/system=yes

echo -e '\n[*] Remove node labels'
all_nodes=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')
for node in "${all_nodes[@]}"
do
    kubectl label nodes ${node} security-ring-
done

# minikube delete
