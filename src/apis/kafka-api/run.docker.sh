#!/bin/sh

docker build -f Dockerfile -t img-project-m-kafka-api-$1 .

docker run --network mandy --name project-m-kafka-api-$1 -p 8001:8002 -it --detach img-project-m-kafka-api-$1
