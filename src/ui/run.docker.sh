#!/bin/sh

docker build -f ui.Dockerfile -t img-pyzdo-ui-$1 .

docker run --name pyzdo-ui-$1 -p 8000:80 -it --detach img-pyzdo-ui-$1

docker exec -it pyzdo-ui-$1 sh
