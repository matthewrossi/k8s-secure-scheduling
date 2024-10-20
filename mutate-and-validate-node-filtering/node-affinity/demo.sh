#!/bin/bash

set -e # make sure the job fails if any instruction fails

function print_and_create_resource {
    if [ $# -eq 2 ]; then
        echo -e "\n$1"
    fi
    curl -s ${@: -1} | sed -e 's/^/> /'
    kubectl create -f ${@: -1}
}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# minikube start --nodes=4

echo '[*] Install admission control service'
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-audit
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager

echo -e '\n[*] Use Gatekeeper to mutate the node affinity config'
# print_and_create_resource "${SCRIPT_DIR}/policy/add-match-expr-mutation.yaml"
print_and_create_resource "${SCRIPT_DIR}/policy/mutate-node-affinity.yaml"

echo -e '\n[*] Use Gatekeeper to validate the node affinity config'
echo -e '\n[+] Add constraint template'
print_and_create_resource "${SCRIPT_DIR}/policy/template.yaml"
echo -e '\n[+] Add constraint'
print_and_create_resource "${SCRIPT_DIR}/policy/constraint.yaml"

# Run node affinity demo
source "${SCRIPT_DIR}/../../default-node-filtering-options/node-affinity/demo.sh"

echo -e '\n[*] Uninstall admission control service'
helm delete gatekeeper --namespace gatekeeper-system
kubectl delete crd -l gatekeeper.sh/system=yes

# minikube delete
