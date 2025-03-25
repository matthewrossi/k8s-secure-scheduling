#!/usr/bin/env bash

echo "[*] Ensure to"
echo "    1. Have run ./setup.sh"

read -p "Start? [Y/n] " ans
if [[ "$ans" = "" ]]; then ans="yes"; fi
case $ans in
    Y|y|yes) ;;
    *) exit 0 ;;
esac

WRK_THREADS=12
WRK_CONNS=100
WRK_TIME=30s

projroot=$(git rev-parse --show-toplevel)
out="$projroot/test/minikube-servers/results/$(uname -n)-t$WRK_THREADS-c$WRK_CONNS-d$WRK_TIME"
mkdir -p "$out"

for service in $(kubectl get services -l type=web-server -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  wrk -t $WRK_THREADS -c $WRK_CONNS -d $WRK_TIME --latency "http://$(minikube ip):$port" > $out/$name
done
