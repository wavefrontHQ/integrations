
## Exporting AWS ECS Stats to Wavefront using Telegraf

Amazon ECS, input plugin uses the Amazon ECS metadata and stats v2 or [v3][task-metadata-endpoint-v3] API endpoints to gather stats on running containers in a Task.

This task makes use of telegraf-ecs plugin and export stats to Wavefront (https://wavefront.com).

The telegraf agent running on ECS instance enables the input plugin and the output plugin which are ECS and Wavefront respectively.

```
 [[inputs.ecs]]
 
 [[outputs.wavefront]]
```
For further reference, please refer to the documentation - https://github.com/influxdata/telegraf/blob/release-1.18/plugins/inputs/ecs/README.md

### Prerequisites
1. An AWS account
2. A Wavefront proxy installed on AWS.

#### Required: The *ip* of your Wavefront proxy

The Wavefront proxy should be installed and accessible by the Docker host machine.

```
{
     "name": "WAVEFRONT_PROXY",

     "value": "YOUR_WAVEFRONT_PROXY_ADDRESS"
}
```

Source tag value for metrics is collected by the telegraf agent running on EC2 instance. This is usually set to the containerID.

#### Required: The *port* of your Wavefront proxy

The Wavefront proxy port is required to connect to Wavefront through the proxy.

```
{

     "name": "WAVEFRONT_PROXY_PORT",

     "value": "YOUR_WAVEFRONT_PROXY_PORT"
}
```

#### Optional: The *ECS_CONTAINER_METADATA_ENDPOINT* of your Wavefront proxy

To enforce the task metadata v2 endpoint, the endpoint URL should be mentioned in the Task Definition as below.

Configuration (enforce v2 metadata):

```
{
    "name": "ECS_CONTAINER_METADATA_ENDPOINT",

    "value": "http://169.254.170.2"
}
```
The amazon-ecs-agent (though it is a container running on the host) is not present in the metadata/stats endpoints.
