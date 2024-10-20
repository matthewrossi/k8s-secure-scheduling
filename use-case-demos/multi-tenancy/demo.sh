#!/bin/bash

set -e # make sure the job fails if any instruction fails

declare -a TENANTS=("uc1" "uc2") #"uc3" "uc4")

function deploy {
    echo -e "\n[*] Deploy $2"
    kubectl create -f "$1"
    kubectl apply -f "$2"

    if [ ${kind} != "pod" ]; then
        sleep 1 # wait for all pods to show up
    fi

    echo -e "\n[+] Pod's node selector"
    kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.namespace == "glaciation-platform" or .metadata.namespace == "uc1" or .metadata.namespace == "uc2") | "\(.metadata.namespace) namespace -> \(.spec.nodeSelector)"'

    echo -e '\nWaiting for the deployment...'
    if [ ${kind} == "pod" ]; then
        kubectl wait -f "$2" --for=condition=Ready
    else
        kubectl rollout status -f "$2"
    fi

    echo -e '\n[+] Pod schedules'
    echo "NAMESPACE, NAME, NODE"
    kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.namespace == "glaciation-platform" or .metadata.namespace == "uc1" or .metadata.namespace == "uc2") | "\(.metadata.namespace), \(.metadata.name), \(.spec.nodeName)"'

    echo -e '\n[+] Delete pod'
    kubectl delete -f "$2"
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

nodes=$(kubectl get nodes -l !node-role.kubernetes.io/control-plane -o json | jq -r '.items[].metadata.name')
readarray -t nodes <<<"${nodes}"
echo -e '\n[*] Set node labels'
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} tenant=${TENANTS[${RANDOM} % 2]} --overwrite # % 4]} --overwrite
done

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
kubectl create -f "${SCRIPT_DIR}/policy/template.yaml"
echo -e '[+] Add constraint'
kubectl create -f "${SCRIPT_DIR}/policy/constraint.yaml"

if [ ${kind} == "pod" ]; then
    deploy "${SCRIPT_DIR}/resources/namespaces.yaml" "${SCRIPT_DIR}/resources/pods.yaml"
else
    deploy "${SCRIPT_DIR}/resources/namespaces.yaml" "${SCRIPT_DIR}/resources/deployments.yaml"
fi

# # Wait for manual interaction with the example application
# echo ''
# read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Delete Gatekeeper resources'
kubectl delete -f "${SCRIPT_DIR}/policy/constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/template.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/mutation.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/expansion-template.yaml"

echo -e '\n[*] Uninstall admission control service'
helm delete gatekeeper --namespace gatekeeper-system
kubectl delete crd -l gatekeeper.sh/system=yes

echo -e '\n[*] Remove node labels'
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} tenant-
done

# minikube delete
