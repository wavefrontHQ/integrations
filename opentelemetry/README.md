# OpenTelemetry Prometheus Collector 


This demo presents the typical flow of observability data with
OpenTelemetry Collectors deployed:

- Applications send data directly to a Collector configured to use fewer
 resources, aka the _agent_;
- The Collector then sends the data to the appropriate backend, in this sample
 Prometheus;

This sample uses `docker-compose` and by default runs against the 
`otel/opentelemetry-collector-dev:latest` image:

```shell
docker-compose up -d
```

The demo exposes the following backends:

- Prometheus at http://0.0.0.0:9090 

Notes:

- It may take some time for the application metrics to appear on the Prometheus
 dashboard;

To clean up any docker container from the demo run `docker-compose down`.

