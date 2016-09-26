# Docker Integration (cAdvisor)

This directory contains resources for monitoring Docker with Wavefront using Google cAdvisor. Please see https://community.wavefront.com/docs/DOC-1208 for more instructions on using.

## Exporting cAdvisor Stats to Wavefront

cAdvisor supports exporting stats to Wavefront (https://wavefront.com). Below are the additional command line arguments needed to tell cAdvisor to export stats to your local Wavefront proxy.

### What You'll Need
1. A Wavefront account.
2. A Wavefront proxy installed on your network.

Set the storage driver to Wavefront.

```
 -storage_driver=wavefront
```

Additional Arguments

#### Required: The *ip:port* of your Wavefront proxy

The proxy should be installed on your network and accessible by the Docker host machine.

 `-storage_driver_wf_proxy_host=ip:port`

#### Required: Source

Source tag value for metrics collected by this cAdvisor instance. We usually recommend setting this to the hostname of the docker host (not the container hostname)

`-storage_driver_wf_source=mydockerhost`

#### Optional: Metric Prefix

It will default to "cadvisor." if not set.

`-storage_driver_wf_prefix=cadvisor.`

#### Optional: Flush Interval

This will default to 10 seconds if not set.

`-storage_driver_wf_interval=10`

#### Optional: Additional Tags

This a string of additional tags that will be applied to every metric.

`-storage_driver_wf_add_tags="az=us-west1 env=dev"`

#### Optional: Taggify Labels

Defaults to true. Determines whether docker labels should be added as point tags to metrics.

`-storage_driver_wf_taggify_labels=true`


# Examples

## Docker Run

```
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  wavefronthq/cadvisor:latest \
  -storage_driver=wavefront \
  -storage_driver_wf_source=$(hostname) \
  -storage_driver_wf_proxy_host=YOUR_PROXY_HOST:2878
```

## Docker Compose

```
cadvisor:
  container_name: cadvisor
  image: wavefronthq/cadvisor:latest
  command: -storage_driver=wavefront -storage_driver_wf_source=$(hostname) -storage_driver_wf_proxy_host=YOUR_PROXY_HOST:2878
  restart: always
  ports:
    - "8080:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:rw
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
```
