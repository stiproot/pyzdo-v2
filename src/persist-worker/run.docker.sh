#!/bin/sh

docker build -f Dockerfile -t img-pyzdo-persist-worker-$1 .

docker run --name pyzdo-persist-worker-$1 \
    -it --detach \
    -e KAFKA_BOOTSTRAP_SERVERS= \
    -e KAFKA_SECURITY_PROTOCOL=SASL_SSL \
    -e KAFKA_SASL_MECHANISMS=PLAIN \
    -e KAFKA_SASL_USERNAME= \
    -e KAFKA_SASL_PASSWORD= \
    -e KAFKA_GROUP_ID=pyzdo-persist-worker-001 \
    -e KAFKA_AUTO_OFFSET_RESET=latest \
    -e WORKER_TOPIC=pyzdo_CMD_PERSIST \
    -e STORE_COMMAND_URL=http://localhost:8000/store/cmd \
    -e STORE_BULK_COMMAND_URL=http://localhost:8000/store/cmds \
    -e STORE_QUERY_URL=http://localhost:8000/store/qry \
    -e ENVIRONMENT=aks \
    -e DEBUGGING=True \
    -e COSMOS_DATABASE_NAME= \
    -e AZURE_CLIENT_ID=\
    -e AZURE_CLIENT_SECRET=\
    -e AZURE_TENANT_ID= \
    img-pyzdo-persist-worker-$1

