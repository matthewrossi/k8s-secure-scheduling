#!/usr/bin/env bash

# NOTE: In order to customize existing tests (e.g., density, load,
# scheduler-throughput) to our test environment multiple variables need to be
# set. Look into their config.yaml file for a complete list of the variables

# With scheduler-throughput (and small clusters of 3 control-plane and 5 worker
# nodes):
# CL2_SCHEDULER_THROUGHPUT_PODS=500
# CL2_DEFAULT_QPS=50
# CL2_DEFAULT_BURST=100
# CL2_UNIFORM_QPS=50
# CL2_SCHEDULER_THROUGHPUT_THRESHOLD=40

NODES="${NODES:-100}"
TEST="${TEST:-scheduler-throughput}" # density, load, scheduler-throughput

cwd=$(pwd)
mkdir -p $cwd/result/$TEST-test

# NOTE: Requires cloning https://github.com/kubernetes/perf-tests and move into
# the perf-tests/clusterloader2 directory
cd $CLUSTERLOADER_PATH
./run-e2e.sh --logtostderr=false --log_file=$cwd/result/$TEST-test.log \
    --report-dir=$cwd/result/$TEST-test --testconfig=./testing/$TEST/config.yaml \
    --nodes=$NODES --provider=kind --kubeconfig=$HOME/.kube/config --v=2
cd $cwd

echo -e "\nLook into $cwd/result/$TEST-test for the measurements"
