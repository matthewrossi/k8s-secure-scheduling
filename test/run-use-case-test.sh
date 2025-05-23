#!/usr/bin/env bash

NODES="${NODES:-100}"
TEST="${TEST:-multi-tenancy}" # options: data-sovereignty, multi-tenancy, workload-security-rings

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ "$BASELINE" = false ]; then
    # Apply labels
    POLICY=$TEST $SCRIPT_DIR/update-labels.sh
    echo

    # Apply policies
    POLICY=$TEST $SCRIPT_DIR/update-policy.sh
    echo
fi

if [ "$TEST" = "multi-tenancy" ]; then
    echo -e "[*] Create namespaces"
    kubectl apply -f $SCRIPT_DIR/use-case/namespaces.yaml
    echo
fi

# Create result directory
mkdir -p $SCRIPT_DIR/result/use-case/$TEST-test

# NOTE: The clusterloader binary has been built from
# https://github.com/kubernetes/perf-tests/tree/master/clusterloader2

# NOTE: To customize the test according to our test environment the following
# variables need to be set
# For example, with a small cluster of 3 control-plane and 10 worker nodes:
# CL2_SCHEDULER_THROUGHPUT_PODS=300 (10) / 3000 (100) / 30000 (1000)
# CL2_DEFAULT_QPS=50
# CL2_DEFAULT_BURST=100
# CL2_UNIFORM_QPS=50
# CL2_SCHEDULER_THROUGHPUT_THRESHOLD=40
echo -e "[*] Run $TEST test"
CL2_PROMETHEUS_NODE_SELECTOR='node-role.kubernetes.io/control-plane: ""' \
CL2_PROMETHEUS_TOLERATE_MASTER=true \
    $SCRIPT_DIR/clusterloader --alsologtostderr --logtostderr=false \
    --enable-prometheus-server=true \
    --tear-down-prometheus-server=false \
    --prometheus-apiserver-scrape-port=6443 \
    --prometheus-pvc-storage-class=standard \
    --prometheus-ready-timeout=0 \
    --log_file=$SCRIPT_DIR/result/use-case/$TEST-test.log \
    --report-dir=$SCRIPT_DIR/result/use-case/$TEST-test \
    --testsuite=$SCRIPT_DIR/use-case/$TEST/scheduler-suite.yaml \
    --nodes=$NODES --provider=kind --kubeconfig=$HOME/.kube/config --v=2

echo -e "Look into $SCRIPT_DIR/result/use-case/$TEST-test for the measurements\n"

if [ "$TEST" = "multi-tenancy" ]; then
    echo -e "[*] Delete namespaces"
    kubectl delete -f $SCRIPT_DIR/use-case/namespaces.yaml
    echo
fi

if [ "$BASELINE" = false ]; then
    # Remove policies
    DELETE=true POLICY=$TEST $SCRIPT_DIR/update-policy.sh
    echo

    # Remove labels
    DELETE=true POLICY=$TEST $SCRIPT_DIR/update-labels.sh
fi
