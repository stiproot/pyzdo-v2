#!/bin/sh

docker build -f Dockerfile -t img-pyzdo-persist-worker-$1 .

docker run --network pyzdo_pyzdo --name pyzdo-persist-worker-$1 -it --detach img-pyzdo-persist-worker-$1
