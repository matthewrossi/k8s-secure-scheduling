#!/usr/bin/env bash

echo "[*] Ensure to"
echo "    1. Run ./setup.sh"
echo "    2. Have a kubectl proxy running"

read -p "Start? [Y/n] " ans
if [[ "$ans" = "" ]]; then ans="yes"; fi
case $ans in
    Y|y|yes) ;;
    *) exit 0 ;;
esac

SERVERS=(nginx apache lighttpd)
WRAPPERS=(default qemu gvisor)

projroot=$(git rev-parse --show-toplevel)
out="$projroot/test/minikube-servers/results"
mkdir -p $out

for server in "${SERVERS[@]}"; do
  for wrapper in "${WRAPPERS[@]}"; do
    pod="$server-$wrapper"
    echo "[*] Testing pod $pod"
    wrk -t12 -c100 -d5s --latency http://localhost:8001/api/v1/namespaces/default/pods/$pod/proxy/ > $out/$pod
  done
done
