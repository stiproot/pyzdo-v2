#!/bin/sh

docker build -f Dockerfile.ui-api -t img-project-m-ui-api-$1 .

docker run --name project-m-ui-api-$1 -p 3001:80 -it --detach img-project-m-ui-api-$1

# docker exec -it projectm-ui-$1 sh
