#!/bin/sh

docker build -f Dockerfile -t img-pyzdo-store-api-$1 .

docker run --name pyzdo-store-api-$1 \
    -p 8005:8001 \
    -e ENVIRONMENT=aks \
    -e KEY_VAULT_URL= \
    -e COSMOS_DATABASE_NAME= \
    -e COSMOS_URL= \
    -e STORE_QUERY_URL= \
    -it --detach \
    img-pyzdo-store-api-$1
