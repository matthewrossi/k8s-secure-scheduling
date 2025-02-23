#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters (expected 4)"
    exit 1
fi

if [ "$1" = false ] ; then
  kubectl create namespace "$2"
fi

# iterate $count number of times
for (( i=1; i<=$3; i++ ))
do
  # generate YAML configuration using heredoc with COUNT variable substitution
  yaml=$(cat <<-END
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fake-pod-$i
  namespace: $2
spec:
  replicas: $4
  selector:
    matchLabels:
      app: fake-pod
  template:
    metadata:
      labels:
        app: fake-pod
    spec:
      # affinity:
      #   nodeAffinity:
      #     requiredDuringSchedulingIgnoredDuringExecution:
      #       nodeSelectorTerms:
      #       - matchExpressions:
      #         - key: type
      #           operator: In
      #           values:
      #           - kwok
      # A taints was added to an automatically created Node.
      # You can remove taints of Node or add this tolerations.
      # tolerations:
      # - key: "kwok.x-k8s.io/node"
      #   operator: "Exists"
      #   effect: "NoSchedule"
      containers:
      - name: fake-container
        image: fake-image
END
)
  if [ "$1" = false ] ; then
    # apply the generated configuration to Kubernetes cluster
    echo "$yaml" | kubectl apply -f -
  else
    # delete the generated configuration to Kubernetes cluster
    echo "$yaml" | kubectl delete -f -
  fi
done

if ! [ "$1" = false ] ; then
  kubectl delete namespace "$2"
fi
