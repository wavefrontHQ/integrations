# nagios-wf.py

## Configuration sample

### Metrics
```
service_perfdata_file=[PATH_PERFDATA]/service-perfdata
service_perfdata_file_template=DATATYPE::SERVICEPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tSERVICEDESC::$SERVICEDESC$\tSERVICEPERFDATA::$SERVICEPERFDATA$\tSERVICECHECKCOMMAND::$SERVICECHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$\tSERVICESTATE::$SERVICESTATE$\tSERVICESTATETYPE::$SERVICESTATETYPE$

service_perfdata_file_mode=a
service_perfdata_file_processing_interval=15
service_perfdata_file_processing_command=wavefront_perf_service

host_perfdata_file=[PATH_PERFDATA]/host-perfdata
host_perfdata_file_template=DATATYPE::HOSTPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tHOSTPERFDATA::$HOSTPERFDATA$\tHOSTCHECKCOMMAND::$HOSTCHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$

host_perfdata_file_mode=a
host_perfdata_file_processing_interval=15
host_perfdata_file_processing_command=wavefront_perf_host
```

```
define command {
    command_name  wavefront_perf_host
    command_line  /opt/nagios/etc/wf/nagios-metrics-wf.py [PATH_PERFDATA]/host-perfdata \
                                                           --wf_proxy_addr [WAVEFRONT_PROXY_ADR] \
                                                           --wf_proxy_port [WAVEFRONT_PROXY_PORT]
}

define command {
    command_name  wavefront_perf_service
    command_line  /opt/nagios/etc/wf/nagios-metrics-wf.py [PATH_PERFDATA]/service-perfdata \
                                                          --service \
                                                          --wf_server [WAVEFRONT_URL] \
                                                          --wf_token [WAVEFRONT_TOKEN]
}
```

### Events
```
define contact{
  name                            wf-generic-contact
  register                        0

  service_notification_period     24x7
  service_notification_options    w,u,c,r,f,s
  service_notification_commands   nagios-to-wavefront-service

  host_notification_period        24x7
  host_notification_options       d,u,r,f,s
  host_notification_commands      nagios-to-wavefront-host
}

define contact{
  contact_name    wfuser
  use             wf-generic-contact
  alias           Sam
  email           sam@foo.com
  address1        +155512312
}

define contactgroup{
  contactgroup_name  wavefront
  alias              Notifications send to wavefront
  members            wfuser
}

define command{
  command_name nagios-to-wavefront-service
  command_line /opt/nagios/etc/wf/nagios-events-wf.py -S \
                                                      --type '$NOTIFICATIONTYPE$' \
                                                      --host '$HOSTNAME$' \
                                                      --service '$SERVICEDISPLAYNAME$' \
                                                      --time '$TIMET$' \
                                                      --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' \
                                                      [WAVEFRONT_URL] \
                                                      [WAVEFRONT_TOKEN]
}

define command{
  command_name nagios-to-wavefront-host
  command_line /opt/nagios/etc/wf/nagios-events-wf.py --type '$NOTIFICATIONTYPE$' \
                                                      --host '$HOSTNAME$' \
                                                      --time '$TIMET$' \
                                                      --msg '$HOSTOUTPUT$' \
                                                      [WAVEFRONT_URL] \
                                                      [WAVEFRONT_TOKEN]
}
```
