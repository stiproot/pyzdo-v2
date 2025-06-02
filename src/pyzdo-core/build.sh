#!/bin/bash

rm -rf dist/

python3 -m build

cd dist/

tar -xvf *.tar.gz -C .
