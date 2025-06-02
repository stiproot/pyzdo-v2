#!/bin/bash

python -m pip uninstall pyzdo_core
python3.11 -m pip uninstall pyzdo_core

python -m pip install dist/pyzdo_core-0.0.1/.
python3.11 -m pip install dist/pyzdo_core-0.0.1/.

cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/workers/persist/tmp/
cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/workers/azdo/tmp/
cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/workers/insights/tmp/
cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/workers/azdo_proxy/tmp/
cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/apis/store-api/tmp/
cp -f dist/pyzdo_core-0.0.1.tar.gz ~/code/azdo/Internal-pyzdoetrics/src/apis/kafka-api/tmp/
