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
