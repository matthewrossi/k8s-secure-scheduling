#!/usr/bin/env bash

projroot=$(git rev-parse --show-toplevel)
out="$projroot/test/minikube-servers/results/$(uname -n)-db"
mkdir -p "$out"

for service in $(kubectl get services -l type=db -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  ./ycsb-0.17.0/bin/ycsb.sh load redis -P ./ycsb-0.17.0/workloads/workloada -p "redis.host=$(minikube ip)" -p "redis.port=$port" > "$out/$name-load"
  ./ycsb-0.17.0/bin/ycsb.sh run redis -P ./ycsb-0.17.0/workloads/workloada -p "redis.host=$(minikube ip)" -p "redis.port=$port" > "$out/$name-run"
done
