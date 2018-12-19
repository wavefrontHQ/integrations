#!/usr/bin/python

import os
import argparse
import urllib2
import json
import urllib
import urllib2
import sys

def doMain():
	msg = args.msg[0].replace("\\n","\r").rstrip()
	annotations = {}
	annotations['severity'] = args.type[0]
	annotations['type'] = 'Nagios'
	annotations['details'] = msg

	notif = {}
	if args.S is not None:
		notif['name'] = "Nagios event on '{}' at '{}'".format(args.service,args.host[0])
	else:
		notif['name'] = "Nagios event at '{}'".format(args.host[0])
	notif['startTime'] = args.time[0]
	notif['endTime'] = args.time[0]+1
	notif['hosts'] = args.host
	notif['annotations'] = annotations

	# http_logger = urllib2.HTTPSHandler(debuglevel = 1)
	# opener = urllib2.build_opener(http_logger) # put your other handlers here too!
	# urllib2.install_opener(opener)

	url = "{}/api/v2/event".format(args.server[0])
	print(url)

	body = json.dumps(notif)
	headers = {}
	headers["Authorization"] = "Bearer {} ".format(args.token[0])
	headers["Content-type"] = "application/json"
	headers["Accept"] = "application/json"

	req = urllib2.Request(url, body, headers)
	response = urllib2.urlopen(req)
	res_body = response.read()
	result = json.loads(res_body)
	if result['status'] is None or result['status']['code'] != 200:
		print(res_body)
		sys.exit(-1)
	else:
		print("OK")
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('server', type=str, nargs=1, help='Wavefront Server URL.')
	parser.add_argument('token', type=str, nargs=1, help='Wavefront token.')
	parser.add_argument('-S', action='store_true', help='Service notification.')
	parser.add_argument('--type', type=str, nargs=1, help='Notification type.')
	parser.add_argument('--host', type=str, nargs=1, help='Notification hostname.')
	parser.add_argument('--service', type=str, nargs='?', help='Notification service name.')
	parser.add_argument('--time', type=int, nargs=1, help='Notification time (UNIX epoch).')
	parser.add_argument('--msg', type=str, nargs=1, help='Notification message.')

	args = parser.parse_args()

doMain()
