# Readme

This script collects metrics from Apache Impala and outputs them in JSON format. This is used together with Telegraf's Exec Input plugin.

### Setup

- Copy the script onto each Impala node.
- This script uses the Requests library. Eensure that it is installed on each node: `pip install requests`

### Usage:

`python impala.py <Impala Daemon server address>:25000 <Impala Statestore server address>:25010 <Impala Catalog server address>:25020`

Enter one or more server addresses depending on which Impala services are on the node.\
Port 25000 is the default web UI port for Impala Daemons. Modify if a different port was configured.\
Port 25010 is the default web UI port for the Impala Statestore. Modify if a different port was configured.\
Port 25020 is the default web UI port for the Impala Catalog Server. Modify if a different port was configured.

