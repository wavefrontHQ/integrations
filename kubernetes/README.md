# Kubernetes Integration

This directory contains resources for monitoring Kubernetes with Wavefront. Please see https://community.wavefront.com/docs/DOC-1204 for instructions on using.

## Additional Configuration Options

`deploy/heapster.yml` defines the ReplicationController for the Heapster container. Line 28 is where the Wavefront sink is defined. This command line argument is what tells Heapster to flush metrics to Wavefront.

```
--sink=wavefront:wavefront-proxy:2878
```

This line can be changed to pass additional options to the Wavefront sink:

```
--sink=wavefront:<proxy address:port>?clusterName=<name of K8s cluster>&prefix=<metric prefix>&includeLabels=<true | false>&includeContainers=<true | false>
```

- `--sink=wavefront:<proxy address:port>`` - Heapster will flush metrics to this address. If you're using the example Wavefront proxy yaml files in `/deploy` - this address will always be `wavefront-proxy:2878`
- `clusterName` - Defaults to _k8s-cluster_ - The name of your K8s cluster. The value is added as a tag called _cluster_ on all metrics.
- `prefix` - Defaults to _heapster._ - The prefix to add to metrics sent by Heapster.
- `includeLabels` - Defaults to _false_ - When set to true, this will add any kubernetes labels as point tags to your metrics.
- `includeContainers` - Defaults to _true_ - When set to false, it will exclude collecting metrics on containers. It will still collect and aggregate metrics about any running pods, but it will skip the child containers.
