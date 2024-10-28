#!/bin/bash

# set -e # make sure the job fails if any instruction fails

echo -e '\n[*] Uninstall admission control web UI'
helm delete gatekeeper-policy-manager --namespace gatekeeper-system

echo -e '\n[*] Uninstall admission control service'
helm delete gatekeeper --namespace gatekeeper-system
kubectl delete crd -l gatekeeper.sh/system=yes

