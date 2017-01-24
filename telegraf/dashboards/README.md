To deploy the Telegraf dashabord on your Wavefront instance:

```
curl -O https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/dashboards/telegraf-host.json
curl -vX POST https://YOUR_INSTANCE.wavefront.com/api/dashboard -d @K8s.json \
  -H "Content-Type: application/json" -H 'X-AUTH-TOKEN: YOUR_API_TOKEN'
  ```

  Replace _YOUR_INSTANCE_ and _YOUR_API_TOKEN_.
