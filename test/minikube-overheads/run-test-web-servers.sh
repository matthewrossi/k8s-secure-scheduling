#!/usr/bin/env bash

WRK_THREADS=1
WRK_CONNS=100
WRK_TIME=120s

projroot=$(git rev-parse --show-toplevel)
out="$projroot/test/minikube-overheads/results/$(uname -n)-web-servers-t$WRK_THREADS-c$WRK_CONNS-d$WRK_TIME"
mkdir -p "$out"

for service in $(kubectl get services -l type=web-server -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  # Warmup
  wrk -t $WRK_THREADS -c $WRK_CONNS -d 30s --latency "http://$(minikube ip):$port" > /dev/null
  # Actual test
  wrk -t $WRK_THREADS -c $WRK_CONNS -d $WRK_TIME --latency "http://$(minikube ip):$port" > $out/$name
done
