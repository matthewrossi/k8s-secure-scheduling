#!/usr/bin/env bash

NODES="${NODES:-100}"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

TEST=data-sovereignty $SCRIPT_DIR/run-use-case-test.sh
TEST=multi-tenancy $SCRIPT_DIR/run-use-case-test.sh
TEST=workload-security-rings $SCRIPT_DIR/run-use-case-test.sh
