#!/bin/bash

set -e # make sure the job fails if any instruction fails

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function deploy {
    set +e # ignore errors

    echo -e "\n[*] Deploy $1"
    kubectl apply -f "$1"

    echo -e "\n[+] Pod's node selector"
    kubectl get -f "$1" -o json | jq -c '.spec.nodeSelector'

    echo -e '\nWaiting for the deployment...'
    kubectl wait -f "$1" --for=condition=Ready --timeout=5s || true

    echo -e '\n[+] Pod status'
    kubectl get pods -o wide

    # echo -e '\n[+] Pod description'
    # kubectl describe -f "$1"

    echo -e '\n[+] Delete pod'
    kubectl delete -f "$1"

    set -e # do not ignore errors
}

# minikube start --nodes=4

echo '[*] Nodes'
kubectl get nodes

nodes=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')

echo -e '\n[*] Set node labels'
count=1
for node in ${nodes}
do
    kubectl label nodes ${node} security_level=${count} --overwrite
    count=$((count+1))
done

echo -e '\n[*] Node labels'
kubectl get nodes --show-labels

deploy "${SCRIPT_DIR}/pod-no-security-level.yaml"
deploy "${SCRIPT_DIR}/pod-specific-security-level.yaml"
deploy "${SCRIPT_DIR}/pod-nonexistent-security-level.yaml"

# # Wait for manual interaction with the example application
# echo ''
# read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Remove node labels'
for node in ${nodes}
do
    kubectl label nodes ${node} security_level-
done

# minikube delete
