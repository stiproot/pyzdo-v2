#!/bin/sh

rm -r ./dist/
npm run build
cp .env ./dist/

docker build -f Dockerfile -t img-pyzdo-ui-$1 .

docker run --name pyzdo-ui-$1 \
    -p 8080:8081 \
    -it --detach \
    img-pyzdo-ui-$1

# docker exec -it pyzdo-ui-$1 sh
