
## Exporting AWS ECS Stats to Wavefront using Telegraf

Amazon ECS, input plugin uses the Amazon ECS metadata and stats v2 or [v3][task-metadata-endpoint-v3] API endpoints to gather stats on running containers in a Task.

The wavefronthq/aws-ecs-wavefront container configured with telegraf must be run in the same Task as the workload it is inspecting to export stats to Wavefront (https://wavefront.com) output plugin.

This is similar to (and reuses a few pieces of) the Docker input plugin, with some ECS specific modifications for AWS metadata and stats formats.

The task metadata endpoint is enabled by default on Amazon ECS EC2 instance based on the Amazon ECS container agent version. To enforce the task metadata v2 endpoint, the endpoint URL should be mentioned as below.

Configuration (enforce v2 metadata):

`{`

    "name": "ECS_CONTAINER_METADATA_ENDPOINT",
    "value": "http://169.254.170.2"
`}`

The amazon-ecs-agent (though it is a container running on the host) is not present in the metadata/stats endpoints.

Below are the additional properties that are required for Telegraf to export stats to your local Wavefront proxy.

### Prerequisites
1. An AWS account
2. A Wavefront proxy installed on AWS.

The docker image comprises a telegraf.conf file which is used to configure the input plugin and the output plugin which are ECS and Wavefront respectively. 

` [[inputs.ecs]]`

` [[outputs.wavefront]]`

### Additional Arguments

#### Required: The *ip* of your Wavefront proxy

The proxy should be installed on AWS network and accessible by the Docker host machine.

`{`

     "name": "WAVEFRONT_PROXY",

     "value": "YOUR_WAVEFRONT_PROXY_ADDRESS"
 `}`

Source tag value for metrics is collected by the telegraf agent running on EC2 instance. This is usually set to the containerID.

#### Required: The *port* of your Wavefront proxy

The wavefront proxy port is required to connect to wavefront through the proxy.

`{`

     "name": "WAVEFRONT_PROXY_PORT",

     "value": "YOUR_WAVEFRONT_PROXY_PORT"
`}`
```
