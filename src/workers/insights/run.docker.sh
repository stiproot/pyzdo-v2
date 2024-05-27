#!/bin/sh

docker build -f Dockerfile -t img-project-m-insights-worker-$1 .

docker run --network project-m_mandy --name project-m-insights-worker-$1 -it --detach img-project-m-insights-worker-$1
