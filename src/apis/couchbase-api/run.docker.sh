#!/bin/sh

docker build -f Dockerfile -t img-project-m-cb-api-$1 .

docker run --network mandy --name project-m-cb-api-$1 -p 8000:8001 -it --detach img-project-m-cb-api-$1
