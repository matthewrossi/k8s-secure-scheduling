#!/bin/bash

set -e # make sure the job fails if any instruction fails

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

declare -a EU_REGIONS=("francecentral" "francesouth" "germanynorth" "germanywestcentral" "italynorth" "northeurope" "norwayeast" "norwaywest" "polandcentral" "spaincentral" "swedencentral" "switzerlandnorth" "switzerlandwest" "westeurope" "eu-central-1" "eu-central-2" "eu-north-1" "eu-south-1" "eu-south-2" "eu-west-1" "eu-west-3" "europe-central2" "europe-north1" "europe-southwest1" "europe-west1" "europe-west3" "europe-west4" "europe-west6" "europe-west8" "europe-west9" "europe-west12")
declare -a US_REGIONS=("centralus" "centraluseuap" "centralusstage" "eastus" "eastus2" "eastus2euap" "eastus2stage" "eastusstage" "eastusstg" "northcentralus" "northcentralusstage" "southcentralus" "southcentralusstage" "southcentralusstg" "westcentralus" "westus" "westus2" "westus2stage" "westus3" "westusstage" "us-east-1" "us-east-2" "us-gov-east-1" "us-gov-west-1" "us-west-1" "us-west-2" "us-central1" "us-east1" "us-east4" "us-east5" "us-south1" "us-west1" "us-west2" "us-west3" "us-west4")
declare -a REGIONS=("italynorth" ${EU_REGIONS[${RANDOM} % 31]} ${US_REGIONS[${RANDOM} % 35]})

function deploy {
    print_section_title "\n[*] Deploy $1"
    pe "kubectl apply -f \"$1\""

    if [ ${kind} != "pod" ]; then
        sleep 1 # wait for all pods to show up
    fi

    print_section_title "\n[.] Pod's node affinity"
    if [ ${kind} == "pod" ]; then
        pe "kubectl get -f \"$1\" -o json | jq -r '.items[] | \"\(.metadata.name) name -> \(.spec.affinity)\"'"
    else
        pe "kubectl get pods -o json | jq -r '.items[] | \"\(.metadata.name) name -> \(.spec.affinity)\"'"
    fi

    print_section_title '\nWaiting for the deployment...'
    if [ ${kind} == "pod" ]; then
        pe "kubectl wait -f \"$1\" --for=condition=Ready"
    else
        pe "kubectl rollout status -f \"$1\""
    fi

    print_section_title "\n[.] Node labels"
    pe "kubectl get nodes -o \"jsonpath={range .items[*]}{.metadata.name}{'\ttopology.kubnernetes.io/region='}{.metadata.labels.topology\.kubernetes\.io/region}{'\n'}{end}\""

    print_section_title '\n[.] Pod schedules'
    pe "kubectl get pods -o wide"

    wait # test cleanup

    print_section_title '\n[.] Delete pod'
    pe "kubectl delete -f \"$1\""
}

function print_section_title {
    echo -n $'\e[32;1m'
    echo -e "$1"
    echo -n $'\e[0m'
}

source "${SCRIPT_DIR}/../demo-magic.sh" -n

# Speed at which to simulate typing
TYPE_SPEED=30

# minikube start --nodes=8

kind="${1:-pod}"

if [ ${kind} != "pod" ] && [ ${kind} != "deployment" ]
then
    echo 'Invalid argument value. Valid argument values are: pod (default), deployment'
    exit 1
fi

nodes=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')
readarray -t nodes <<<"${nodes}"

# Set node labels
i=0
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} topology.kubernetes.io/region=${REGIONS[${i} % 3]} --overwrite
    i=$((i+1))
done

clear
wait # avoid seeing command prompt

print_section_title "[*] Let's see the nodes part of our Kubernetes cluster"
pe "kubectl get nodes -o \"jsonpath={range .items[*]}{.metadata.name}{'\ttopology.kubnernetes.io/region='}{.metadata.labels.topology\.kubernetes\.io/region}{'\n'}{end}\""

if [[ $install ]]; then
    source "${SCRIPT_DIR}/../../gatekeeper-install.sh"
else
    print_section_title "\n[*] Let's see what is running in our Kubernetes cluster"
    pe 'kubectl get pods --namespace gatekeeper-system'

    print_section_title '\n[*] External services'
    print_section_title '\n[.] Gatekeeper Policy Manager'
    pe 'export URL=http://$(kubectl get ingress -n gatekeeper-system gatekeeper-policy-manager -o jsonpath="{.spec.rules[0].host}")'
    pe 'echo "Serving Gatekeeper Policy Manager at $URL"'
fi

wait # show nodes labels and web UI

print_section_title '\n[*] Allow Gatekeeper to reject workloads that create pods violating constraints'
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/expansion-template.yaml\""

print_section_title '\n[*] Use Gatekeeper to mutate the node affinity config'
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/mutation.yaml\""

print_section_title '\n[*] Use Gatekeeper to validate the node affinity config'
print_section_title '[.] Add constraint template'
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/template.yaml\""
print_section_title '[.] Add constraints'
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/ensure-data-soverignty-constraint.yaml\""
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/warn-unknown-eu-region-constraint.yaml\""
pe "kubectl apply -f \"${SCRIPT_DIR}/policy/warn-unknown-us-region-constraint.yaml\""

wait # show web UI

if [ ${kind} == "pod" ]; then
    deploy "${SCRIPT_DIR}/resources/pods.yaml"
else
    deploy "${SCRIPT_DIR}/resources/deployments.yaml"
fi

print_section_title '\n[*] Delete Gatekeeper resources'
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/warn-unknown-eu-region-constraint.yaml\""
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/warn-unknown-us-region-constraint.yaml\""
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/ensure-data-soverignty-constraint.yaml\""
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/template.yaml\""
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/mutation.yaml\""
pe "kubectl delete -f \"${SCRIPT_DIR}/policy/expansion-template.yaml\""

if [[ $install ]]; then
    source "${SCRIPT_DIR}/../../gatekeeper-uninstall.sh"
fi

wait # avoid seeing command prompt

# Remove node labels
for node in "${nodes[@]}"
do
    kubectl label nodes ${node} topology.kubernetes.io/region-
done

# minikube delete
