#!/usr/bin/python

import argparse
import platform
import time
import os
import re
import logging

from wavefront_sdk.client_factory import WavefrontClientFactory


def main():
    newFileName = args.file + "." + str(int(time.time()))
    count = 0
    try:
        if not args.test:
            logging.info("moving: ''" + args.file + "' to '" + newFileName + "'")
            os.rename(args.file, newFileName)
        else:
            newFileName = args.file
        logging.info("processing: '" + newFileName + "'")
        try:
            with open(newFileName) as f:
                for line in f:
                    process(line)
                    count = count + 1
        finally:
            if not args.test:
                os.remove(newFileName)
    except FileNotFoundError:
        pass
    wavefront_client.send_metric("nagios.metrics.processed.per.execution", count, time.time(), platform.node(), {})


def process(line):
    info = extractInfo(line)
    print(info)

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
            wavefront_client.send_metric(metricName, re.sub(r"[^0-9.]", "", value.lower()), info["TIMET"], info["HOSTNAME"], tags)
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
    parser.add_argument('--wf_server', dest="server", help='Wavefront Server URL.')
    parser.add_argument('--wf_token', dest="token", help='Wavefront token.')
    parser.add_argument('--wf_proxy_addr', dest="addr", help='Wavefront Proxy address.')
    parser.add_argument('--wf_proxy_port', dest="port", help='Wavefront Proxy port.')
    parser.add_argument('--csp_base_url', dest= "csp_base_url", help='Base URL of CSP console.')
    parser.add_argument('--csp_api_token', dest="csp_api_token", help='CSP API Token for csp authentication.')
    parser.add_argument('--csp_app_id', dest="csp_app_id", help='CSP OAuth App ID for csp authentication.')
    parser.add_argument('--csp_app_secret', dest="csp_app_secret", help='CSP OAuth App secret for csp authentication.')
    parser.add_argument('--csp_org_id', dest="csp_org_id", help='CSP Organization ID for csp authentication.')

    args = parser.parse_args()
    logging.info(args)

    client_factory = WavefrontClientFactory()
    if args.addr is not None and args.port is not None:
        proxy_address = "proxy://{}:{}".format(args.addr, args.port)
        client_factory.add_client(
            url=proxy_address,
            max_queue_size=50000,
            batch_size=10000,
            flush_interval_seconds=5)
    elif args.server is not None and args.token is not None:
        wavefront_server = args.server[:8] + args.token + '@' + args.server[8:]
        client_factory.add_client(
            url=args.server,
            max_queue_size=50000,
            batch_size=10000,
            flush_interval_seconds=5)
    elif args.csp_base_url is not None and args.csp_api_token is not None and args.server is not None:
        client_factory.add_client(
            url=args.server,
            csp_base_url=args.csp_base_url,
            csp_api_token=args.csp_api_token,
            csp_org_id=args.csp_org_id,
            max_queue_size=50000,
            batch_size=10000,
            flush_interval_seconds=5)
    elif args.server is not None and args.csp_base_url is not None and args.csp_app_id is not None and \
            args.csp_app_secret is not None:
        client_factory.add_client(
            url=args.server,
            csp_base_url=args.csp_base_url,
            csp_app_id=args.csp_app_id,
            csp_app_secret=args.csp_app_secret,
            csp_org_id=args.csp_org_id,
            max_queue_size=50000,
            batch_size=10000,
            flush_interval_seconds=5)
    else:
        parser.print_help()
        exit(-1)

    wavefront_client = client_factory.get_client()
    print(wavefront_client)

    try:
        startTime = time.time()
        main()
        endTime = time.time()
        wavefront_client.send_metric("nagios.script.execution.time", (endTime - startTime), endTime, platform.node(), {})
    finally:
        # If the application failed to send metrics/histograms/tracing-spans,
        # you can get the total failure count as follows:
        total_failures = wavefront_client.get_failure_count()

        # On-demand buffer flush
        wavefront_client.flush_now()

        # Close the sender connection
        wavefront_client.close()

