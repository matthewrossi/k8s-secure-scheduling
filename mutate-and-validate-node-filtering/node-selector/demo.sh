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

source "${SCRIPT_DIR}/../../gatekeeper-install.sh"

echo -e '\n[*] Use Gatekeeper to mutate the node affinity config'
print_and_create_resource "${SCRIPT_DIR}/policy/mutate-node-selector.yaml"

echo -e '\n[*] Use Gatekeeper to validate the node affinity config'
echo -e '\n[+] Add constraint template'
print_and_create_resource "${SCRIPT_DIR}/policy/template.yaml"
echo -e '\n[+] Add constraint'
print_and_create_resource "${SCRIPT_DIR}/policy/constraint.yaml"

# Run node affinity demo
source "${SCRIPT_DIR}/../../default-node-filtering-options/node-selector/demo.sh"

source "${SCRIPT_DIR}/../../gatekeeper-uninstall.sh"

# minikube delete
