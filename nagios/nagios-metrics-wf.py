#!/usr/bin/python

import argparse
import time
import os
import re
import logging

from wavefront_sdk import WavefrontDirectClient
from wavefront_sdk import WavefrontProxyClient

def main():
	newFileName = args.file + "." + str(int(time.time()))
	if args.test == False:
		logging.info("moving: ''" + args.file +"' to '" + newFileName+ "'")
		os.rename(args.file, newFileName)
	else:
		newFileName = args.file

	logging.info("processing: '" + newFileName + "'")

	try:
		with open(newFileName) as f:
		    for line in f:
		        process(line)
	finally:
		if args.test == False:
			os.remove(newFileName)

def process(line):
	info = extractInfo(line)

	metrics = info["SERVICEPERFDATA"] if args.service else info["HOSTPERFDATA"]
	for metirc,value in extractValues(metrics).items():
		metricName = "nagios."
		metricName += ("service" if args.service else "host") + "."
		metricName += (info["SERVICEDESC"]+".") if args.service else ""
		metricName +=  metirc

		tags = {}
		tags["HOSTSTATE"] = info["HOSTSTATE"]
		tags["HOSTSTATETYPE"] = info["HOSTSTATETYPE"]
		if args.service:
			tags["SERVICECHECKCOMMAND"] = info["SERVICECHECKCOMMAND"]
			tags["SERVICESTATETYPE"] = info["SERVICESTATETYPE"]
			tags["SERVICESTATE"] = info["SERVICESTATE"]
			tags["SERVICESTATETYPE"] = info["SERVICESTATETYPE"]
		else:
			tags["HOSTCHECKCOMMAND"] = info["HOSTCHECKCOMMAND"]

		try:
			logging.info(">> metricName: "+metricName)
			client.send_metric(metricName, re.sub(r"[^0-9.]", "", value.lower()), info["TIMET"], info["HOSTNAME"], tags)
		except ValueError as e:
			print(e)

def extractValues(valuesStr):
	values = {}
	if len(valuesStr) > 0:
		for value in valuesStr.split(" "):
			k,v = value.split("=",1)
			values[k] = v.split(";",1)[0]
	logging.info(values)
	return values

def extractInfo(line):
	info = {}
	for prop in line.split("\t"):
		k,v = prop.split("::",1)
		info[k] = v
	return info

if __name__== "__main__":
	parser = argparse.ArgumentParser(description='Sends Nagios perfdata to wavefront.')
	parser.add_argument('file')
	parser.add_argument('--service', dest='service', action='store_true',
						help='proccess "service-perfdata" (default: "host-perfdata")')
	parser.add_argument('--test', dest='test', action='store_true')
	parser.add_argument('--wf_server', dest="server")
	parser.add_argument('--wf_token', dest="token")
	parser.add_argument('--wf_proxy_addr', dest="addr")
	parser.add_argument('--wf_proxy_port', dest="port")

	args = parser.parse_args()
	logging.info(args)

	if args.addr is not None and args.port is not None :
		client = WavefrontProxyClient(host=args.addr,
		                              metrics_port=args.port,
		                              distribution_port=40000,
		                              tracing_port=30000)
	elif args.server is not None and args.token is not None :
		client = WavefrontDirectClient(server=args.server,
		                               token=args.token ,
		                               max_queue_size=50000,
		                               batch_size=10000,
		                               flush_interval_seconds=15)
	else:
		parser.print_help()
		exit(-1)

	try:
		main()
	finally:
		client.close()
