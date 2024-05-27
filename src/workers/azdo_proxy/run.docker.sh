#!/bin/sh

docker build -f Dockerfile -t img-project-m-persist-worker-$1 .

docker run --network project-m_mandy --name project-m-persist-worker-$1 -it --detach img-project-m-persist-worker-$1
