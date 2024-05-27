#!/bin/sh

rm -r ./dist/
npm run build
cp .env ./dist/

docker build -f Dockerfile -t img-project-m-ui-$1 .

docker run --name project-m-ui-$1 \
    -p 8080:8081 \
    -it --detach \
    img-project-m-ui-$1

# docker exec -it projectm-ui-$1 sh
