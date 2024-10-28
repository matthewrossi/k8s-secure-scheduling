#!/bin/bash

# set -e # make sure the job fails if any instruction fails

CURR_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo -e '\n[*] Install admission control service'
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-audit
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager

echo -e '\n[*] Install admission control web UI'
helm repo add gpm https://sighupio.github.io/gatekeeper-policy-manager
helm upgrade --install --namespace gatekeeper-system --set image.tag=v1.0.10 --values ${CURR_SCRIPT_DIR}/values.yaml gatekeeper-policy-manager gpm/gatekeeper-policy-manager

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-policy-manager

export NODE_PORT=$(kubectl get --namespace gatekeeper-system -o jsonpath="{.spec.ports[0].nodePort}" services gatekeeper-policy-manager)
export NODE_IP=$(kubectl get nodes --namespace gatekeeper-system -o jsonpath="{.items[0].status.addresses[0].address}")
echo -e "\nServing Gatekeeper Policy Manager at http://$NODE_IP:$NODE_PORT"

