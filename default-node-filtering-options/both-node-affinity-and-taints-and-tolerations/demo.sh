#!/bin/bash

set -e # make sure the job fails if any instruction fails

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function deploy {
    echo -e "\n[+] Deploy $1"
    kubectl apply -f "$1"

    echo -e "\n[-] Pod's affinity"
    kubectl get -f "$1" -o json | jq -c '.spec.affinity'

    echo -e "\n[-] Pod's tolerations"
    kubectl get -f "$1" -o json | jq -c '.spec.tolerations[:-2]'

    echo -e '\nWaiting for the deployment...'
    kubectl wait -f "$1" --for=condition=Ready --timeout=5s || true

    echo -e '\n[-] Pod status'
    kubectl get pods -o wide

    # echo -e '\n[-] Pod description'
    # kubectl describe -f "$1"

    echo -e '\n[-] Delete pod'
    kubectl delete -f "$1"
}

function run_test {
    nodes=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')

    echo -e '\n[+] Set node labels and taints'
    count=1
    for node in ${nodes}
    do
        # Stop tainting when the target number of nodes is reached
        if [ "$count" -gt "$1" ]; then
            break
        fi

        kubectl label nodes ${node} security_level=${count} --overwrite
        kubectl taint nodes ${node} security_level=${count}:NoSchedule --overwrite
        count=$((count+1))
    done

    echo -e '\n[+] Node labels'
    kubectl get nodes --show-labels

    echo -e '\n[+] Taints'
    kubectl get nodes -o json | jq -r '.items[] | "\(.metadata.name)\t\(.spec.taints)"'

    deploy "${SCRIPT_DIR}/pod-no-security-level.yaml"
    deploy "${SCRIPT_DIR}/pod-specific-security-level.yaml"
    deploy "${SCRIPT_DIR}/pod-multiple-security-levels.yaml"
    deploy "${SCRIPT_DIR}/pod-all-security-levels.yaml"
    deploy "${SCRIPT_DIR}/pod-nonexistent-security-level.yaml"

    # # Wait for manual interaction with the example application
    # echo ''
    # read -n 1 -srep '<<Press any key to continue>>'

    echo -e '\n[+] Remove node labels and taints'
    count=1
    for node in ${nodes}
    do
        # Stop removing the taints when the target number of nodes is reached
        if [ "$count" -gt "$1" ]; then
            break
        fi

        kubectl label nodes ${node} security_level-
        kubectl taint nodes ${node} security_level=${count}:NoSchedule-
        count=$((count+1))
    done
}

# minikube start --nodes=4

echo '[*] Nodes'
kubectl get nodes

echo -e '\n[*] Run tests with taints on all nodes'
run_test 4

echo -e '\n[*] Run tests with taints on all but one nodes'
run_test 3

# minikube delete
