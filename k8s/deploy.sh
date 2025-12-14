#!/bin/bash

kubectl apply -f namespace.yaml

eval $(minikube docker-env)

docker build -t fastapi-app:latest ../ -f ../microservice/Dockerfile


kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgres-pv.yaml

kubectl apply -f postgres.yaml


echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n noter-app --timeout=120s

kubectl apply -f fastapi-app.yaml

echo "Deployment completed. Checking status..."
kubectl get all -n noter-app

minikube service fastapi-service -n noter-app
