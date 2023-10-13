# nagios-wf.py

## Configuration sample

### Metrics
```
service_perfdata_file=[PATH_PERFDATA]/service-perfdata
service_perfdata_file_template=DATATYPE::SERVICEPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tSERVICEDESC::$SERVICEDESC$\tSERVICEPERFDATA::$SERVICEPERFDATA$\tSERVICECHECKCOMMAND::$SERVICECHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$\tSERVICESTATE::$SERVICESTATE$\tSERVICESTATETYPE::$SERVICESTATETYPE$

service_perfdata_file_mode=a
service_perfdata_file_processing_interval=15
service_perfdata_file_processing_command=wavefront-perf-service

host_perfdata_file=[PATH_PERFDATA]/host-perfdata
host_perfdata_file_template=DATATYPE::HOSTPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tHOSTPERFDATA::$HOSTPERFDATA$\tHOSTCHECKCOMMAND::$HOSTCHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$

host_perfdata_file_mode=a
host_perfdata_file_processing_interval=15
host_perfdata_file_processing_command=wavefront-perf-host
```

#### Using CSP API Token
```
define command {
    command_name  wavefront-perf-host
    command_line /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]/host-perfdata \
                                                           --wf_server [WAVEFRONT_URL] \
                                                           --csp_api_token [CSP_API_TOKEN] \
                                                           --csp_base_url [CSP_BASE_URL]                                                         
}

define command {
    command_name  wavefront-perf-service
    command_line /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]/service-perfdata \
                                                           --service \
                                                           --wf_server [WAVEFRONT_URL] \
                                                           --csp_api_token [CSP_API_TOKEN] \
                                                           --csp_base_url [CSP_BASE_URL]
}
```

#### Using CSP Oauth
```
define command {
    command_name  wavefront-perf-host
    command_line /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]//host-perfdata \
                                                           --wf_server [WAVEFRONT_URL] \
                                                           --csp_app_id [CSP_APP_ID] \
                                                           --csp_app_secret [CSP_APP_SECRET] \
                                                           --csp_base_url [CSP_BASE_URL]                                                        
}

define command {
    command_name  wavefront-perf-service
    command_line /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]/service-perfdata \
                                                           --service \
                                                           --wf_server [WAVEFRONT_URL] \
                                                           --csp_app_id [CSP_APP_ID] \
                                                           --csp_app_secret [CSP_APP_SECRET] \
                                                           --csp_base_url [CSP_BASE_URL]
}
```

#### Using Wavefront Ingestion
```
define command {
    command_name  wavefront-perf-host
    command_line  /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]//host-perfdata \
                                                           --wf_proxy_addr [WAVEFRONT_PROXY_ADR] \
                                                           --wf_proxy_port [WAVEFRONT_PROXY_PORT]
 }


define command {
    command_name  wavefront-perf-service
    command_line  /usr/local/nagios/libexec/nagios-metrics-wf.py [PATH_PERFDATA]/service-perfdata \
                                                           --service \
                                                           --wf_server [WAVEFRONT_URL] \
                                                           --wf_token [WAVEFRONT_TOKEN]
}
```

Refer the configuration samples at https://github.com/wavefrontHQ/integrations/raw/master/nagios/config to send metrics using CSP API token, CSP Oauth or Wavefront API Token.

### Contacts

Add the below Contact and Contact group to the `contacts.cfg`.

```
# Wavefront contact definition for event notification commands
define contact {
  name                            wf-generic-contact
  register                        0

  service_notification_period     24x7
  service_notification_options    w,u,c,r,f,s
  service_notification_commands   nagios-to-wavefront-service

  host_notification_period        24x7
  host_notification_options       d,u,r,f,s
  host_notification_commands      nagios-to-wavefront-host
}

# Wavefront user definition
define contact {
  contact_name    wfuser
  use             wf-generic-contact
  alias           Admin
  email           admin@example.com
  address1        +155512312
}

# Contact group for Wavefront user definition
define contactgroup {
  contactgroup_name  wavefront
  alias              Notifications send to wavefront
  members            wfuser
}
```

### Events
#### Using CSP API Token
```
define command {
    command_name nagios-to-wavefront-host
    command_line /usr/local/nagios/libexec/nagios-events-wf.py --type '$NOTIFICATIONTYPE$' \
                                                        --host '$HOSTNAME$' --time '$TIMET$' \
                                                        --msg '$HOSTOUTPUT$' \
                                                        --wf_server [WAVEFRONT_URL] \
                                                        --csp_api_token [CSP_API_TOKEN] \
                                                        --csp_base_url [CSP_BASE_URL]
}


define command {
    command_name nagios-to-wavefront-service
    command_line /usr/local/nagios/libexec/nagios-events-wf.py -S --type '$NOTIFICATIONTYPE$' \
                                                        --service '$SERVICEDISPLAYNAME$' \
                                                        --host '$HOSTNAME$' --time '$TIMET$' \
                                                        --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' \
                                                        --wf_server [WAVEFRONT_URL] \
                                                        --csp_api_token [CSP_API_TOKEN] \
                                                        --csp_base_url [CSP_BASE_URL]
}
```

#### Using CSP Oauth
 ```
define command {
    command_name nagios-to-wavefront-host
    command_line /usr/local/nagios/libexec/nagios-events-wf.py --type '$NOTIFICATIONTYPE$' \
                                                        --host '$HOSTNAME$' --time '$TIMET$' \
                                                        --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' \
                                                        --wf_server [WAVEFRONT_URL] \
                                                        --csp_app_id [CSP_APP_ID] \
                                                        --csp_app_secret [CSP_APP_SECRET] \
                                                        --csp_base_url [CSP_BASE_URL]
}


define command {
    command_name nagios-to-wavefront-service
    command_line /usr/local/nagios/libexec/nagios-events-wf.py -S --type '$NOTIFICATIONTYPE$' \
                                                        --service '$SERVICEDISPLAYNAME$' \
                                                        --host '$HOSTNAME$' --time '$TIMET$' \
                                                        --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' \
                                                        --wf_server [WAVEFRONT_URL] \
                                                        --csp_app_id [CSP_APP_ID] \
                                                        --csp_app_secret [CSP_APP_SECRET] \
                                                        --csp_base_url [CSP_BASE_URL]
}
 ```

#### Using Wavefront Ingestion
```
define command {
    command_name nagios-to-wavefront-host
    command_line /usr/local/nagios/libexec/nagios-events-wf.py --type '$NOTIFICATIONTYPE$' \
                                                       --host '$HOSTNAME$' \
                                                       --time '$TIMET$' \
                                                       --msg '$HOSTOUTPUT$' \
                                                       --wf_server [WAVEFRONT_URL] \
                                                       --wf_token [WF_API_TOKEN]
}


define command {
    command_name nagios-to-wavefront-service
    command_line /usr/local/nagios/libexec/nagios-events-wf.py -S --type '$NOTIFICATIONTYPE$' \
                                                       --service '$SERVICEDISPLAYNAME$' \
                                                       --host '$HOSTNAME$' --time '$TIMET$' \
                                                       --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' \
                                                       --wf_server [WAVEFRONT_URL] \
                                                       --wf_token [WF_API_TOKEN]
}
```

Refer the configuration samples at https://github.com/wavefrontHQ/integrations/raw/master/nagios/config to send events using CSP API token, CSP Oauth or Wavefront API Token.

