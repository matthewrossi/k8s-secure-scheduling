#!/bin/bash

set -e # make sure the job fails if any instruction fails

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

declare -a EU_REGIONS=("francecentral" "francesouth" "germanynorth" "germanywestcentral" "italynorth" "northeurope" "norwayeast" "norwaywest" "polandcentral" "spaincentral" "swedencentral" "switzerlandnorth" "switzerlandwest" "westeurope" "eu-central-1" "eu-central-2" "eu-north-1" "eu-south-1" "eu-south-2" "eu-west-1" "eu-west-3" "europe-central2" "europe-north1" "europe-southwest1" "europe-west1" "europe-west3" "europe-west4" "europe-west6" "europe-west8" "europe-west9" "europe-west12")
declare -a US_REGIONS=("centralus" "centraluseuap" "centralusstage" "eastus" "eastus2" "eastus2euap" "eastus2stage" "eastusstage" "eastusstg" "northcentralus" "northcentralusstage" "southcentralus" "southcentralusstage" "southcentralusstg" "westcentralus" "westus" "westus2" "westus2stage" "westus3" "westusstage" "us-east-1" "us-east-2" "us-gov-east-1" "us-gov-west-1" "us-west-1" "us-west-2" "us-central1" "us-east1" "us-east4" "us-east5" "us-south1" "us-west1" "us-west2" "us-west3" "us-west4")
declare -a REGIONS=("italynorth" ${EU_REGIONS[${RANDOM} % 31]} ${US_REGIONS[${RANDOM} % 35]})

function deploy {
    echo -e "\n[*] Deploy $1"
    kubectl apply -f "$1"

    if [ ${kind} != "pod" ]; then
        sleep 1 # wait for all pods to show up
    fi

    echo -e "\n[+] Pod's node affinity"
    if [ ${kind} == "pod" ]; then
        kubectl get -f "$1" -o json | jq -r '.items[] | "\(.metadata.name) name -> \(.spec.affinity)"'
    else
        kubectl get pods -o json | jq -r '.items[] | "\(.metadata.name) name -> \(.spec.affinity)"'
    fi

    echo -e '\nWaiting for the deployment...'
    if [ ${kind} == "pod" ]; then
        kubectl wait -f "$1" --for=condition=Ready
    else
        kubectl rollout status -f "$1"
    fi

    echo -e '\n[+] Pod status'
    kubectl get pods -o wide

    echo -e '\n[+] Delete pod'
    kubectl delete -f "$1"
}

# minikube start --nodes=8

kind="${1:-pod}"

if [ ${kind} != "pod" ] && [ ${kind} != "deployment" ]
then
    echo 'Invalid argument value. Valid argument values are: pod (default), deployment'
    exit 1
fi

echo '[*] Nodes'
kubectl get nodes

nodes=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')
readarray -t nodes <<<"${nodes}"
echo -e '\n[*] Set node labels'
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} topology.kubernetes.io/region=${REGIONS[${RANDOM} % 3]} --overwrite
done

echo -e '\n[*] Node labels'
kubectl get nodes --show-labels

source "${SCRIPT_DIR}/../../gatekeeper-install.sh"

echo -e '\n[*] Allow Gatekeeper to reject workloads that create pods violating constraints'
kubectl apply -f "${SCRIPT_DIR}/policy/expansion-template.yaml"

echo -e '\n[*] Use Gatekeeper to mutate the node affinity config'
kubectl apply -f "${SCRIPT_DIR}/policy/mutation.yaml"

echo -e '\n[*] Use Gatekeeper to validate the node affinity config'
echo -e '[+] Add constraint template'
kubectl apply -f "${SCRIPT_DIR}/policy/template.yaml"
echo -e '[+] Add constraints'
kubectl apply -f "${SCRIPT_DIR}/policy/ensure-data-soverignty-constraint.yaml"
kubectl apply -f "${SCRIPT_DIR}/policy/warn-unknown-eu-region-constraint.yaml"
kubectl apply -f "${SCRIPT_DIR}/policy/warn-unknown-us-region-constraint.yaml"

if [ ${kind} == "pod" ]; then
    deploy "${SCRIPT_DIR}/resources/pods.yaml"
else
    deploy "${SCRIPT_DIR}/resources/deployments.yaml"
fi

# Wait for manual interaction with the example application
echo ''
read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Delete Gatekeeper resources'
kubectl delete -f "${SCRIPT_DIR}/policy/warn-unknown-eu-region-constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/warn-unknown-us-region-constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/ensure-data-soverignty-constraint.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/template.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/mutation.yaml"
kubectl delete -f "${SCRIPT_DIR}/policy/expansion-template.yaml"

source "${SCRIPT_DIR}/../../gatekeeper-uninstall.sh"

echo -e '\n[*] Remove node labels'
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} topology.kubernetes.io/region-
done

# minikube delete
