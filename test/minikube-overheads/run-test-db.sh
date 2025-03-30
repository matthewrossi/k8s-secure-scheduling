#!/usr/bin/env bash

projroot=$(git rev-parse --show-toplevel)
out="$projroot/test/minikube-overheads/results/$(uname -n)-nosql-db"
mkdir -p "$out"

for service in $(kubectl get services -l app=redis -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  ./deps/ycsb-0.17.0/bin/ycsb.sh load redis -P ./deps/ycsb-0.17.0/workloads/workloada -p "redis.host=$(minikube ip)" -p "redis.port=$port" > "$out/$name-load"
  ./deps/ycsb-0.17.0/bin/ycsb.sh run redis -P  ./deps/ycsb-0.17.0/workloads/workloada -p "redis.host=$(minikube ip)" -p "redis.port=$port" > "$out/$name-run"
done

for service in $(kubectl get services -l app=mongo -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  ./deps/ycsb-0.17.0/bin/ycsb.sh load mongodb -P ./deps/ycsb-0.17.0/workloads/workloada -p "mongodb.url=mongodb://$(minikube ip):$port" > "$out/$name-load"
  ./deps/ycsb-0.17.0/bin/ycsb.sh run  mongodb -P ./deps/ycsb-0.17.0/workloads/workloada -p "mongodb.url=mongodb://$(minikube ip):$port" > "$out/$name-run"
done

out="$projroot/test/minikube-overheads/results/$(uname -n)-postgres-sysbench"
mkdir -p "$out"
for service in $(kubectl get services -l app=postgres -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  sysbench \
    --db-driver=pgsql \
    --pgsql-host="$(minikube ip)" \
    --pgsql-port=$port \
    --pgsql-password=example \
    --pgsql-user=sbtest \
    oltp_read_write.lua prepare
  sysbench \
    --db-driver=pgsql \
    --pgsql-host="$(minikube ip)" \
    --pgsql-port=$port \
    --pgsql-password=example \
    --pgsql-user=sbtest \
    --percentile=99 \
    oltp_read_write.lua run > "$out/result"
  sysbench \
    --db-driver=pgsql \
    --pgsql-host="$(minikube ip)" \
    --pgsql-port=$port \
    --pgsql-password=example \
    --pgsql-user=sbtest \
    oltp_read_write.lua cleanup
done

out="$projroot/test/minikube-overheads/results/$(uname -n)-postgres-dbt3-$(date +%Y-%m-%dT%H:%M:%S)"
for service in $(kubectl get services -l app=postgres -o name); do
  port=$(kubectl get $service -o json | jq '.spec.ports[0].nodePort')
  echo "[*] Testing $service at $(minikube ip):$port"
  name=$(echo $service | cut -d'/' -f2)
  PGHOST="$(minikube ip)" PGPORT="$port" PGUSER=sbtest PGPASSWORD=example dbt3-run --stats --tpchtools="deps/TPC-H V3.0.1" pgsql "$out/$name"
done
