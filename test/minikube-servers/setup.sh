#!/usr/bin/env bash

kubectl apply -f nginx.yaml
kubectl apply -f apache.yaml
kubectl apply -f lighttpd.yaml

for dep in $(kubectl get deployments -l paper=secure-scheduling -o name); do
  kubectl expose $dep --type=NodePort --port=80
done
