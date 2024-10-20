#!/bin/bash

set -e

echo -e '[*] Install OpenKruise'
helm repo add openkruise https://openkruise.github.io/charts/
helm install kruise openkruise/kruise --version 1.7.2
