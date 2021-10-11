## Envoy Proxy on Kubernetes

### Sample Envoy Proxy Deployment

1. Copy the `envoy-deployment.yaml` and `envoy-configmap.yaml` files into the Kubernetes cluster.

2. Edit the `envoy-configmap.yaml` file and update `<ENVOY_CLUSTER_NAME>`.

3. Run the below commands to create the Envoy ConfigMap and Deployment:
```
kubectl create -f envoy-configmap.yaml
kubectl create -f envoy-deployment.yaml
```
**NOTE**:
* The following annotations snippet are mandatory to scrape envoy metrics by Wavefront Collector.
`Example: envoy-deployment.yaml`
```
template:
  metadata:
    labels:
      app: envoy
    # mandatory annotations to scrape envoy metrics
    annotations:
      prometheus.io/scrape: 'true'
      prometheus.io/port: '9901' # port_value of Envoy ConfigMap
      prometheus.io/path: '/stats/prometheus'
```

* If you have already deployed Envoy Proxy in your Kubernetes cluster and not discovered, then annotate the pods to get discovered by Wavefront Collector:
```
kubectl annotate pods <pod-name> prometheus.io/scrape=true prometheus.io/port=9901 prometheus.io/path=/stats/prometheus
```

### Monitoring Envoy Proxy

If the Wavefront Collector and Proxy are already configured, you should be able to see the envoy metrics on `Envoy Proxy on Kubernetes` dashboard.

If you do not have the Wavefront Collector for Kubernetes installed on your Kubernetes cluster, follow these instructions to add it to your cluster by using [Helm](https://docs.wavefront.com/kubernetes.html#kubernetes-quick-install-using-helm) or performing [Manual Installation](https://docs.wavefront.com/kubernetes.html#kubernetes-manual-install).

**NOTE**: The auto-discovery and annotation based discovery are enabled by default in Wavefront Collector configuration.

```
enableDiscovery: true
...
...
discovery:
  disable_annotation_discovery: false
```
