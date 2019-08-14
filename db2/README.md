
# DB2 RDBMS metric collector

This python script collects metrics from DB2 RDBMS using DB2's performance monitor tables. This script outputs metric in Influx or wavefront format and can be used together with Telegraf's Exec Input plugin to send data to the Wavefront.

## How to set it up and run

You first need to setup a running telegraf agent and have a running Wavefront proxy to receive the metrics collected by the agent.

This document will not dive deep into setting the telegraf agent. [click here to see the instruction on Wavefront docs website](https://docs.wavefront.com/telegraf.html)

### Setting up the appropriate privileges in DB2

This integration will need to connect to the running DB2 instance and be able to run queries on certain monitor performance resources. Switch to the instance master user (e.g. DB2INST1) and run these commands in db2 CLI. You should start the database and connect to the database of your choice before running these.
```
update dbm cfg using HEALTH_MON on  
update dbm cfg using DFT_MON_STMT on  
update dbm cfg using DFT_MON_LOCK on  
update dbm cfg using DFT_MON_TABLE on  
update dbm cfg using DFT_MON_BUFPOOL on
```
Validate whether the settings are correctly applied by running the following command:
```
get dbm cfg
```
Among the configurations being output'ed, you should see the following settings:
```
Default database monitor switches  
  Buffer pool                         (DFT_MON_BUFPOOL) = ON  
  Lock                                   (DFT_MON_LOCK) = ON  
  Sort                                   (DFT_MON_SORT) = OFF  
  Statement                              (DFT_MON_STMT) = ON  
  Table                                 (DFT_MON_TABLE) = ON  
  Timestamp                         (DFT_MON_TIMESTAMP) = ON  
  Unit of work                            (DFT_MON_UOW) = OFF  
Monitor health of instance and databases   (HEALTH_MON) = ON
```
### Installing ibm_db package using pip
The script is in python, so make sure the system has the correct python version. The minimum version required is 2.7.14+
Install the `ibm_db` package using `pip`
```
pip install ibm_db
```
### Setting up the integration using Telegraf's exec plugin
 * Copy the `wavefront_db2_metrics.py` to a location reachable by telegraf service.
 * Create a file called `50-db2.conf` and add the following content:
```
[[inputs.exec]]
 commands = ['python "<path_to_your_script>/wavefront_db2_metrics.py" -s "127.0.0.1" -d "mydb" -U "db2inst1" -P "<password>" -t telegraf -f wavefront']
 timeout = "5s"
 data_format = "wavefront"
```
 * The following parameters are supplied with the script
      * --server (-s) : IP address or the hostname of the DB2 server (required)
      * --port (-p) : Port number of the DB2 server. Default is 50000
      * --db (-d) : DB name of the server (required)
      * --user (-U) : User ID for connecting
      * --passwd (-P) : User Password for connecting
      * --interval (-i) : Time interval (is not used)
      * --debug (-D) : Turn on the debug mode
      * --format (-f) : message output format. Can be `influx` or `wavefront`
      * --type (-t) : output type. Can be `telegraf` or `wf_proxy`. This will actually let you send the data directly to proxy without going through the telegraf, but you need to set the proxy_host and proxy_port manually to use it.
 * Move the file to your telegraf's `telegraf.d` directory. This config will then be picked up by the telegraf when it restarts. The location of the `telegraf.d` directory may vary depending on the operating system. For macOS, the location is usually in `/usr/local/etc/telegraf.d`. For the general Linux, the location is in `/etc/telegraf/telegraf.d`
* Restart the telegraf agent. Details on how to restart the telegraf is found [here](https://docs.wavefront.com/telegraf.html#restart-telegraf)

### Troubleshooting the integration

The integration script will let you unit-test your script by providing -D as an option for `debug` mode, where the output will be sent out to standard output, with additional information such as your current configuration and the actual SQL query being executed.
Also, you can run the script with `-h`option which will print out the help information.

It is generally a good idea to test the script's execution by running it with -D option, and then add it into the telegraf. Also, keep in mind that the user that is running the script and the user that is running the telegraf as a service may be different (telegraf service, when invoked via `systemctl` runs as either root user or telegraf user, depending on how it is set up. Always make sure the telegraf user can execute the proper version of `python` and `ibm_db` and have all the necessary privileges before actually running it.

### Monitoring DB2 using Dashboard

Create a dashboard and copy the content of `wavefront-db2-metrics.json` included with the python script to run and monitor the integration.

By default, metrics will be populated under the prefix `db2.*` in the metrics space. If you have any prefix defined in either on your telegraf or wavefront proxy, you can edit the default prefix that is defined in the Dashboard's dashboard variable, by the name `prefix`


