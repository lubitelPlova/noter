#!/bin/bash

# Создаем namespace
kubectl apply -f namespace.yaml

# Настраиваем docker для использования Minikube
eval $(minikube docker-env)

# Собираем образ FastAPI приложения (предполагается, что Dockerfile в ../microservice/Dockerfile)
docker build -t noter-service:latest ../ -f ../microservice/Dockerfile

# Применяем конфигурацию
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgres-pv.yaml

# Ждем немного перед запуском PostgreSQL
sleep 5

# Запускаем PostgreSQL
kubectl apply -f postgres.yaml

# Ждем пока PostgreSQL запустится
echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n noter-app --timeout=120s

# Запускаем FastAPI приложение
kubectl apply -f fastapi-app.yaml

# Показываем статус
echo "Deployment completed. Checking status..."
kubectl get all -n noter-app

# Открываем приложение в браузере
minikube service fastapi-service -n noter-app
