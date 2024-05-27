#!/bin/sh

docker build -f Dockerfile -t img-project-m-azdo-worker-$1 .

docker run --network project-m_mandy --name project-m-azdo-worker-$1 -it --detach img-project-m-azdo-worker-$1
