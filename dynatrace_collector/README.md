## Overview
The Wavefront Dynatrace collector collects metrics from Dynatrace and pushes to the wavefront.

## Installation

Install using the provided setup.py
- Clone this repository.
- Change directory to dynatrace_collector.
- Run below command to install Dynatrace collector.

```
pip3 install .
```

## Configure Dynatrace Collector
Run Below command to configure Dynatrace Collector.
```
wf-dynatrace config -b <dynatrace-base-url> -a <dynatrace-api-key> -s <wavefront-proxy-ip> 
```

This command will store the configuration data in a secure file and later that data will be used for collecting the data from Dynatrace and sending data to the Wavefront.

## Start Dynatrace Collector
- Running collector in foreground.
```
wf-dynatrace run
```

- Running collector as a daemon.
```
wf-dynatrace run -d true
```

### Dynatrace Collector as Service
- Start collector.
```
dynatrace-collector start
```

- Stop collector.
```
dynatrace-collector stop
```
- Check Service status.
```
dynatrace-collector status
```

- Restart  collector.
```
dynatrace-collector restart
```

### Metrics Configuration
The metrics configuration file will be located in the `/etc/wavefront/dynatrace/config/config.json`, use this configuration file to enable/disable the metrics collection.