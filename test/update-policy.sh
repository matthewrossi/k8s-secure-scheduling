#!/usr/bin/env bash

DELETE="${DELETE:-false}" # options: false, true
POLICY="${POLICY:-multi-tenancy}" # options: data-sovereignty, multi-tenancy, workload-security-rings

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ "$DELETE" = false ]; then
    echo -e '[*] Allow Gatekeeper to reject workloads that create pods violating constraints'
    kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/expansion-template.yaml"

    echo -e '\n[*] Use Gatekeeper to mutate the node affinity/selector config'
    kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/mutation.yaml"

    echo -e '\n[*] Use Gatekeeper to validate the node affinity/selector config'
    echo -e '[+] Add constraint template'
    kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/template.yaml"

    case "$POLICY" in
        'data-sovereignty')
            echo -e '[+] Add constraints'
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/ensure-data-soverignty-constraint.yaml"
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/warn-unknown-eu-region-constraint.yaml"
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/warn-unknown-us-region-constraint.yaml"
            ;;
        'multi-tenancy')
            echo -e '[+] Add constraint'
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/constraint.yaml"
            ;;
        'workload-security-rings')
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/allowed-nodeselector-values-template.yaml"

            echo -e '[+] Add constraint'
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/allowed-nodeselector-values-constraint.yaml"
            kubectl apply -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/constraint.yaml"
            ;;
        *)
            echo "Unknown policy: $POLICY"
            exit 1
            ;;
    esac
else
    echo -e '[*] Delete Gatekeeper resources'
    case "$POLICY" in
        'data-sovereignty')
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/warn-unknown-eu-region-constraint.yaml"
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/warn-unknown-us-region-constraint.yaml"
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/ensure-data-soverignty-constraint.yaml"
            ;;
        'multi-tenancy')
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/constraint.yaml"
            ;;
        'workload-security-rings')
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/allowed-nodeselector-values-constraint.yaml"
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/constraint.yaml"
            kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/allowed-nodeselector-values-template.yaml"
            ;;
        *)
            echo "Unknown policy: $POLICY"
            exit 1
            ;;
    esac

    kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/template.yaml"
    kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/mutation.yaml"
    kubectl delete -f "${SCRIPT_DIR}/../use-case-demos/$POLICY/policy/expansion-template.yaml"
fi
