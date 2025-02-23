#!/usr/bin/env bash

NAMESPACE="${NAMESPACE:-test}"
COUNT="${COUNT:-100}"
REPLICAS="${REPLICAS:-100}"
DELETE="${DELETE:-false}"

echo "[*] Run simple test"
./deployment.sh $DELETE $NAMESPACE $COUNT $REPLICAS
