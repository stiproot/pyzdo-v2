#!/bin/bash

kubectl apply -f project-m-ui.yml
kubectl apply -f project-m-ui-api.yml
kubectl apply -f project-m-store-api.yml
kubectl apply -f project-m-kafka-api.yml
kubectl apply -f project-m-azdo-proxy-api.yml
kubectl apply -f project-m-azdo-worker.yml
kubectl apply -f project-m-azdo-proxy-worker.yml
kubectl apply -f project-m-persist-worker.yml
kubectl apply -f project-m-insights-worker.yml

# kubectl apply -f project-m-db.yml
# kubectl apply -f kafka/kafka.yml
# kubectl apply -f kafka/kafka-service.yml