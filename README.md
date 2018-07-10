# Integrations

This repository contains various resources for integrating Wavefront with third-party and open source tools. See [the documentation](https://docs.wavefront.com/label_integrations%20list.html) for the total list of integrations supported by Wavefront.

## Deploying Dashboards

To deploy a custom dashboard on your Wavefront account:

1. Make sure you have a valid API token with API access. This can be retrieved from [your profile page](https://docs.wavefront.com/wavefront_api.html#generating-an-api-token) within Wavefront.
2. Download the dashboard template `.json` file you'd like to deploy.
3. Post the `.json` file using Wavefront's dashboard API:

```
curl -O https://raw.githubusercontent.com/wavefrontHQ/integrations/master/examples/k8s.json
curl -vX POST https://metrics.wavefront.com/api/dashboard -d @k8s.json \
  -H "Content-Type: application/json" -H 'X-AUTH-TOKEN: YOUR_API_TOKEN'
```

Update `YOUR_API_TOKEN` and the URL to your Wavefront cluster.

## Contributing

We welcome pull requests! If you have created a dashboard and/or integration recipe that you would like to share with our community, you can submit a pull request.
