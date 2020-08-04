#!/usr/bin/python

import argparse
import time
import os
import re
import logging

from wavefront_sdk import WavefrontDirectClient
from wavefront_sdk import WavefrontProxyClient


def main():
    newFileName = args.file
    count = 0
    logging.info("processing: '" + newFileName + "'")

    try:
        with open(newFileName, 'r+') as f:
            for line in f:
                process(line)
                count = count + 1
        f.truncate(0)
    except:
        pass
    client.send_metric("nagios.metrics.processed.per.execution", count, time.time(), "localhost", {})


def process(line):
    info = extractInfo(line)

    metrics = info["SERVICEPERFDATA"] if args.service else info["HOSTPERFDATA"]
    for metric, value in list(extractValues(metrics).items()):
        metricName = "nagios."
        metricName += ("service" if args.service else "host") + "."
        metricName += (info["SERVICEDESC"] + ".") if args.service else ""
        metricName += metric

        tags = {"HOSTSTATE": info["HOSTSTATE"], "HOSTSTATETYPE": info["HOSTSTATETYPE"]}
        if args.service:
            tags["SERVICECHECKCOMMAND"] = info["SERVICECHECKCOMMAND"]
            tags["SERVICESTATETYPE"] = info["SERVICESTATETYPE"]
            tags["SERVICESTATE"] = info["SERVICESTATE"]
            tags["SERVICESTATETYPE"] = info["SERVICESTATETYPE"]
        else:
            tags["HOSTCHECKCOMMAND"] = info["HOSTCHECKCOMMAND"]

        try:
            logging.info(">> metricName: " + metricName)
            metricName = convert_key_to_wf_metric(metricName)
            client.send_metric(metricName, re.sub(r"[^0-9.]", "", value.lower()), info["TIMET"], info["HOSTNAME"], tags)
        except ValueError as e:
            print(e)


def extractValues(valuesStr):
    values = {}
    if len(valuesStr) > 0:
        for value in valuesStr.split(" "):
            k, v = value.split("=", 1)
            values[k] = v.split(";", 1)[0]
    logging.info(values)
    return values


def extractInfo(line):
    info = {}
    for prop in line.split("\t"):
        k, v = prop.split("::", 1)
        info[k] = v
    return info


def convert_key_to_wf_metric(key):
    """ A Wavefront metric name can be: 'Any lowercase, alphanumeric, dot-separated value. May also
    include dashes (-) or underscores (_)' """
    metric = replace_punctuation_and_whitespace(key)
    metric = remove_trailing_dots(metric)
    metric = just_one_dot(metric)
    metric = metric.lower()
    return metric


def replace_punctuation_and_whitespace(text):
    """Replace occurrences of punctuation (other than . - _) and any consecutive white space with ."""
    rx = re.compile(r"[^\w\s\-.]|\s+")
    return rx.sub(".", text)


def just_one_dot(text):
    """Some metrics can end up with multiple . characters. Replace with a single one"""
    rx = re.compile(r"\.+")
    return rx.sub(".", text)


def remove_trailing_dots(text):
    """Remove any trailing . characters from a metric name"""
    rx = re.compile(r"\.+$")
    return rx.sub("", text)


if __name__ == "__main__":
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

    if args.addr is not None and args.port is not None:
        client = WavefrontProxyClient(host=args.addr,
                                      metrics_port=args.port,
                                      distribution_port=40000,
                                      tracing_port=30000)
    elif args.server is not None and args.token is not None:
        client = WavefrontDirectClient(server=args.server,
                                       token=args.token,
                                       max_queue_size=50000,
                                       batch_size=10000,
                                       flush_interval_seconds=15)
        print(client)
    else:
        parser.print_help()
        exit(-1)

    try:
        startTime = time.time()
        main()
        endTime = time.time()
        client.send_metric("nagios.script.execution.time", (endTime - startTime), endTime, "localhost", {})
    finally:
        client.close()

