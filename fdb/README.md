# FoundationDB metrics collector

This script collects the metrics from FoundationDB and outputs in influx format. This is used together with Telegraf's exec Input plugin.

##### Setup:
- ###### Install FoundationDB Client
    - Download the FoundationDB client rmp `foundationdb-clients-*.el7.x86_64.rpm`form [here](https://apple.github.io/foundationdb/downloads.html).
    - Install the download rpm.

- ###### Install FoundationDB python API library
    - Download the FoundationDB python API library `foundationdb-*.tar.gz`form [here](https://apple.github.io/foundationdb/downloads.html).
    - Untar the download file.
    - Install the download library by executing the setup.py.
    - Test the installation by just importing the `fdb`.
    - Download the [FoundationDB Metrics Collector](https://raw.githubusercontent.com/wavefrontHQ/integrations/master/fdb/fdb-metrics-collector.py).

##### Usage:
- python fdb-metrics-collector.py  `FoundationDB Cluster File Path`

##### Example:
- python fdb-metrics-collector.py  /etc/foundationdb/fdb.cluster
