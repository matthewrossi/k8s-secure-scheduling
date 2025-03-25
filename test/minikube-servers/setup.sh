#!/usr/bin/env bash

# -------------- Web servers

kubectl apply -f nginx.yaml
kubectl apply -f apache.yaml
kubectl apply -f lighttpd.yaml

# -------------- Databases

kubectl apply -f redis.yaml

# -------------- Expose everything

for dep in $(kubectl get deployments -l type=web-server -o name); do
  kubectl expose $dep --type=NodePort --port=80
done
for dep in $(kubectl get deployments -l app=redis -o name); do
  kubectl expose $dep --type=NodePort --port=6379
done

# -------------- Check for YCSB

if [[ ! -f 'ycsb-0.17.0.tar.gz' ]]; then
  rm -rf ycsb-0.17.0
  curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-0.17.0.tar.gz
  tar xfvz ycsb-0.17.0.tar.gz
fi
