#!/bin/bash

python -m pip uninstall pm_common
python3.11 -m pip uninstall pm_common

python -m pip install dist/pm_common-0.0.1/.
python3.11 -m pip install dist/pm_common-0.0.1/.

cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/workers/persist/tmp/
cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/workers/azdo/tmp/
cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/workers/insights/tmp/
cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/workers/azdo_proxy/tmp/
cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/apis/store-api/tmp/
cp -f dist/pm_common-0.0.1.tar.gz ~/code/azdo/Internal-ProjectMetrics/src/apis/kafka-api/tmp/
