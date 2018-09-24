# FoundationDB data collector

This script collects the data from FoundationDB, and outputs in influx format. This is used together with Telegraf's Exec Input plugin.

Usage:
- Copy the script onto the Foundation DB Node and execute the below command.
- python fdb.py  `FoundationDB Cluster File Path`

Example:
python fdb.py  /etc/foundationdb/fdb.cluster