## Overview
The Wavefront Dynatrace collector collects metrics from Dynatrace and pushes to the wavefront.

## Prerequisites
Install below packages:
- gcc
- python-devel

## Installation

Install using the provided setup.py
- Clone this repository.
- Change directory to dynatrace_collector.
- Run below command to install Dynatrace collector:

```
pip install .
```

## Configure Dynatrace Collector
Running a command via the command line is the simplest method. Run Below command to configure Dynatrace collector.
```
wf-dynatrace config -b <dynatrace-base-url> -a <dynatrace-api-key> -s <wavefront-proxy-ip> -p <wavefront_proxy_metric_port>
```

 `wf-dynatrace config` command has the following command-line options:

| Argument | Required?       | Description |
| -------- | ------------ | ----------- |
| -b | True    | Dynatrace base URL, e.g. `https://your-cluster.dynatrace.com` |
| -a | True | Dynatrace API key |
| -s | True | Wavefront proxy IP |
| -p | False | Wavefront proxy metric port, Default is `2878`  |

This command will store the configuration data in a secure file and later that data will be used for collecting the data from Dynatrace and sending data to the Wavefront.

## Start Dynatrace Collector
- Running collector in foreground
```
wf-dynatrace run
```

- Running collector as a daemon
```
wf-dynatrace run -d true
```

### Dynatrace Collector as Service
- Start collector
```
dynatrace-collector start
```

- Stop collector
```
dynatrace-collector stop
```
- Check Service status
```
dynatrace-collector status
```

- Restart  collector
```
dynatrace-collector restart
```

### Metrics Configuration
The metrics configuration file will be located in the `/opt/wavefront/dynatrace/config/config.json`, use this configuration file to enable/disable the metrics collection.

Configuration options:

| Options | Description |
| -------- | ----------- |
| family | Filter the metrics based on family, to disable the metric for any family remove an entire object from the array |
| detailedSources | It filters metrics based on detailed source name. This can be found in the metric definition |
| displayNameRegexPattern | It filters metrics based on the entity display name. Value can be an entity display name or any regex pattern, default is `all`  |

### Troubleshooting
Log file will be located in the `/tmp/wavefront/dynatrace/log/dynatrace.log`.