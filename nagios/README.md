# nagios-wf.py

## Configuration sample

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
	command_line /opt/nagios/etc/wf/nagios-wf.py -S --type '$NOTIFICATIONTYPE$' --host '$HOSTNAME$' --service '$SERVICEDISPLAYNAME$' --time '$TIMET$' --msg '$SERVICEOUTPUT$\n$NOTIFICATIONAUTHOR$\n$NOTIFICATIONCOMMENT$' https://nimba.wavefront.com 6490a634-ca7d-47c1-bb04-4629f53fc98b
}

define command{
	command_name nagios-to-wavefront-host
	command_line /opt/nagios/etc/wf/nagios-wf.py --type '$NOTIFICATIONTYPE$' --host '$HOSTNAME$' --time '$TIMET$' --msg '$HOSTOUTPUT$' https://nimba.wavefront.com 6490a634-ca7d-47c1-bb04-4629f53fc98b
}
```
