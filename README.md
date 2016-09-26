# Integrations

This repository contains various resources and examples for integrating Wavefront with third-party and open source tools.

# Deploying Dashboards

Many of the applications listed in this repository contain example dashboards in the form of .json files. To deploy a dashboard on your Wavefront account:

1. Make sure you have a valid API token with API access. This can be retrieved from [your profile page](https://metrics.wavefront.com/settings/profile) within Wavefront.
2. Download the dashboard template .json file you'd like to add.
3. Post the .json file using Wavefront's dashboard API.

### Example
```
curl -O https://raw.githubusercontent.com/wavefrontHQ/integrations/master/kubernetes/dashboards/K8s.json
curl -vX POST https://metrics.wavefront.com/api/dashboard -d @K8s.json \
  -H "Content-Type: application/json" -H 'X-AUTH-TOKEN: YOUR_API_TOKEN'
```

Just be sure to update _YOUR_API_TOKEN_ and the URL to your Wavefront cluster (if needed).

# Contributing

We welcome pull requests! If you have created a dashboard and/or integration recipe that you would like to share with our community, you can either submit a pull request directly or contact support@wavefront.com.
