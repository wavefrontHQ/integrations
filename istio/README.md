## Configuring Prometheus to scrape Istio metrics

The Prometheus server scrapes the Istio application pods (envoy-proxy) directly to get all the HTTP and TCP metrics. These metrics will have a very high cardinality. To resolve this, we need to create the `recording rules` which aggregate and remove the pod_name and unnecessary labels from the metrics and a job to scrape only the `federated metrics`.

#### Sample recording rule:
```
    groups:
    - name: istio.workload.istio_request_duration_milliseconds_bucket
      interval: 10s
      rules:

      - record: federate:istio_request_duration_milliseconds_bucket
        expr: |
          sum(irate(istio_request_duration_milliseconds_bucket{job="kubernetes-pods"}[1m]))
          by (
            app,
            reporter,
            response_code,
            response_flags,
            source_workload,
            source_workload_namespace,
            destination_workload,
            destination_workload_namespace,
            le
          )

    - name: istio.federate.request_duration.histogram
      interval: 10s
      rules:
      - record: federate:istio_request_duration_milliseconds_bucket_p50
        expr: |
          histogram_quantile(0.5, federate:istio_request_duration_milliseconds_bucket)

      - record: federate:istio_request_duration_milliseconds_bucket_p75
        expr: |
          histogram_quantile(0.75, federate:istio_request_duration_milliseconds_bucket)

      - record: federate:istio_request_duration_milliseconds_bucket_p90
        expr: |
          histogram_quantile(0.90, federate:istio_request_duration_milliseconds_bucket)

      - record: federate:istio_request_duration_milliseconds_bucket_p95
        expr: |
          histogram_quantile(0.95, federate:istio_request_duration_milliseconds_bucket)

      - record: federate:istio_request_duration_milliseconds_bucket_p99
        expr: |
          histogram_quantile(0.99, federate:istio_request_duration_milliseconds_bucket)

      - record: federate:istio_request_duration_milliseconds_bucket_p999
        expr: |
          histogram_quantile(0.999, federate:istio_request_duration_milliseconds_bucket)
```

#### Configuring federated job:
```
    scrape_configs:
    - job_name: federate
      scrape_interval: 15s
      honor_labels: true
      metrics_path: /federate
      params:
        'match[]':
          - '{__name__=~"federate:(.*)"}'
          - '{job=~"federate|kubernetes-pods"}'

      static_configs:
      - targets:
        - prometheus:9090
      metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'federate:(.*)'
        target_label: __name__
        action: replace
```
In this scrape config, we are instructing Prometheus to scrape metrics with the prefix `federate:` from the job `federate` and then to remove the prefix `federate:`
Example, the metric `federate:istio_requests_total`  becomes `istio_requests_total`.


To push these federated metrics to Wavefront, the Prometheus source in `Wavefront Collector for Kubernetes` has to be configured to scrape the Prometheus end-point `/federate`. For more info refer to [Istio integration](https://docs.wavefront.com/istio.html#istio-setup) document.
