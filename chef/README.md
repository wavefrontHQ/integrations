# Chef data collector
This script collects metrics from Chef Server and outputs into JSON format.
This can be used together with Telegraf's Exec Input plugin to send data to the Wavefront.

## Usage:
- Install the Reporting server on Chef server using the below commands:
```
	   chef-server-ctl install opscode-reporting
	   chef-server-ctl reconfigure
	   opscode-reporting-ctl reconfigure
```
- Download this script onto your Chef server, and place it in an accessible location, for example `/etc/telegraf/.chef`
- Keep the private key of the Chef user in a file in an accessible location, for example `/etc/telegraf/.chef/admin.pem`
- Create the file `knife.rb` on your Chef server with the following configuration settings for your environment, and place it in an accessible location, for example `/etc/telegraf/.chef`
```
	   # Sample for chef_server_url is: "https://chef.wavefront.com/organizations/bu"
	   chef_server_url          << Chef Server Url >>
	   # Sample for node_name is: "admin"
	   node_name                << Node Name >>
	   # Sample for client_name is: "admin"
	   client_name              << Client Name >>
	   # Sample for client_key is: "/etc/telegraf/.chef/admin.pem"
	   # client_key should be path of the file from step 2
	   client_key               << Client Key File Path>>
	   ssl_verify_mode          :verify_none
	   log_level                :info
	   log_location             STDOUT
```
- Test the script execution using this command:
```
    /opt/opscode/bin/knife exec -c /etc/telegraf/.chef/knife.rb /etc/telegraf/.chef/chef-metrics-collector
```
- You should get a response such as the following:
```
{
	      "server.nodes_count": 2,
	      "server.cookbooks_count": 11,
	      "server.roles_count": 1,
	      "server.environments_count": 1,
	      "server.rabbitmq_messages_ready": 0,
	      "server.postgresql_seq_scan": 1820630,
	      "server.postgresql_seq_tup_read": 213945431,
	      "server.postgresql_idx_scan": 13817008,
	      "server.postgresql_idx_tup_fetch": 12098595,
	      "server.postgresql_n_tup_ins": 8689,
	      "server.postgresql_n_tup_upd": 1365,
	      "server.postgresql_n_tup_del": 4639,
	      "server.postgresql_n_live_tup": 14980,
	      "server.postgresql_n_dead_tup": 841,
	      "server.postgresql_connection_count": 26,
	      "server.status": 1,
	      "server.rest_api": 1,
	      "server.sql_db": 1,
	      "server.index": 1,
	      "server.run_success": 0,
	      "server.run_failure": 0,
	      "server.run_aborted": 0
}
```
**Note**: If the script does not execute, adjust the file permissions and the path to the `knife` executable.
