## VMware Blockchain Setup

rm that enables multi-party workflows. It uses advanced techniques such as byzantine fault-tolerant state machine replication, authenticated data structures, and integration with smart contract execution engines to enable customers to build and run decentralized multi-party applications.
### Step 1. Install the Wavefront Proxy

If you do not have a [Wavefront proxy](https://docs.wavefront.com/proxies.html) installed on your network, [install a proxy](/proxies/add).

### Step 2. Install PyYAML and Jinja2

Install PyYAML package of version 5.4.1 or greater
  ```
  sudo pip3 install pyyaml
  ```
Install Jinja2 packgae of version 3.0.3
  ```
  sudo pip3 install Jinja2
  ```


### Step 3. Download the VMware Blockchain Scripts

Download the [VMware Blockchain](https://raw.githubusercontent.com/wavefrontHQ/integrations/master/vmware_blockchain) directory.

### Step 4. Run the Blockchain Script

1. Use the [VMware Blockchain script](https://raw.githubusercontent.com/wavefrontHQ/integrations/master/vmware_blockchain/createRules.py) to create the metrics filter required by Wavefront Proxy and allow only few metrics to Wavefront.
2. Update the [metrics_list.txt](https://raw.githubusercontent.com/wavefrontHQ/integrations/master/vmware_blockchain/metrics_list.txt) file with metric names (One metric per line).
3. Run the script: `./createRules.py`. Stop the script by pressing **Control+C**.
4. The script generates the `preprocessor_rules.yaml` file which should be placed under the `/config/wavefront-proxy/` in Wavefront Proxy. Make sure the `preprocessor_rules.yaml` file has the permission 644.
5. The parameter preprocessorConfigFile needs to be set to /config/wavefront-proxy/preprocessor_rules.yaml in `wavefront.conf` as below:
  ```
  preprocessorConfigFile=/config/wavefront-proxy/preprocessor_rules.yaml
  ```
6. Make sure the generated YAML file is valid and formatted. A sample `metrics_list.txt` and `preprocessor_rules.yaml` files are provided for reference.
