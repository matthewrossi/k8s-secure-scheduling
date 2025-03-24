#!/usr/bin/env bash

kubectl apply -f ../env/minikube/nginx.yaml
kubectl apply -f ../env/minikube/apache.yaml
kubectl apply -f ../env/minikube/lighttpd.yaml
