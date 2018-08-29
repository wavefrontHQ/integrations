#!/bin/env bash

#Change the paths for the environment variables appropriate for your environment.
export LD_LIBRARY_PATH=/u01/app/oracle/product/12.1.0/db_1/lib/
export ORACLE_HOME=/u01/app/oracle/product/12.1.0/db_1
export PYTHONPATH=/usr/bin/python3.6
export PATH=PATH:/usr/bin/python3.6
export TNS_ADMIN=$ORACLE_HOME/network/admin
export ORACLE_SID=oradb


#point to the Python install path like '/usr/bin/python' below.
/usr/bin/python3.6 "/etc/telegraf/exec/wavefront_oracle_metrics.py" -u "wavefront" -p "<wavefront-password>" -s "<sid>"
