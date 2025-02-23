#!/usr/bin/env bash

cwd=$(pwd)
mkdir -p $cwd/result/simple-test

# NOTE: Requires cloning https://github.com/kubernetes/perf-tests and move into
# the perf-tests/clusterloader2 directory
cd $CLUSTERLOADER_PATH
go run cmd/clusterloader.go --logtostderr=false --log_file=$cwd/result/simple-test.log \
    --report-dir=$cwd/result/simple-test --testconfig=config.yaml --provider=kind --kubeconfig=$HOME/.kube/config --v=2
cd $cwd

echo -e "\nLook into $cwd/result/simple-test for the measurements"
