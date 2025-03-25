#!/usr/bin/env bash

kubectl delete deployment -l paper=secure-scheduling
kubectl delete service -l paper=secure-scheduling
