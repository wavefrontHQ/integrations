# Readme

This script collects metrics from Apache Kudu Tablet Servers and Masters and outputs in JSON format. This is used together with Telegraf's Exec Input plugin.

Tablet metrics will have a point tag, `table`, which contains the table's name.

### Setup

Copy the script onto each Kudu node.
This script uses the Requests library so ensure that it is installed on each node.

### Usage:

`python kudu.py <Kudu tablet server address>:8050 <Kudu master server address>:8051`

Enter one or more server addresses depending on which Kudu services the node hosts.
Port 8050 is the default web UI port for Kudu Tablet Servers. Modify if a different port was configured.
Port 8051 is the default web UI port for the Kudu Master. Modify if a different port was configured.

