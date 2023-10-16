#!/usr/bin/python

import argparse
import logging

from wavefront_sdk import WavefrontClientFactory


def main():
    msg = args.msg.replace("\\n", "\r").rstrip()
    annotations = {'severity': args.type,
                   'type': 'Nagios',
                   'details': msg}
    startTime = args.time
    endTime = args.time + 1

    if args.service is not None:
        name = "Nagios event on '{}' at '{}'".format(args.service, args.host)
    else:
        name = "Nagios event at '{}'".format(args.host)

    wavefront_client.send_event(name, startTime, endTime, args.host, ["env:", "test-event"], annotations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sends Nagios perfdata to Operations for Applications.')
    parser.add_argument('--wf_server', dest="server", help='Operations for Applications server URL.')
    parser.add_argument('--wf_token', dest="token", help='Operations for Applications API token.')
    parser.add_argument('-S', action='store_true', help='Service notification.')
    parser.add_argument('--type', help='Notification type.')
    parser.add_argument('--host', help='Notification hostname.')
    parser.add_argument('--service', type=str, nargs='?', help='Notification service name.')
    parser.add_argument('--time', type=int, help='Notification time (UNIX epoch).')
    parser.add_argument('--msg', help='Notification message.')
    parser.add_argument('--wf_proxy_addr', dest="addr")
    parser.add_argument('--wf_proxy_port', dest="port")
    parser.add_argument('--csp_base_url', dest="csp_base_url", help='Base URL of the VMware Cloud Services Console.')
    parser.add_argument('--csp_api_token', dest="csp_api_token", help='VMware Cloud services API token.')
    parser.add_argument('--csp_app_id', dest="csp_app_id", help='ID of a server to server OAuth app in VMware Cloud services.')
    parser.add_argument('--csp_app_secret', dest="csp_app_secret", help='Secret of a server to server OAuth app in VMware Cloud services.')
    parser.add_argument('--csp_org_id', dest="csp_org_id", help='Long ID of the VMware Cloud organization running the service. The OAuth app must be added to this organization.')

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
            url=wavefront_server,
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
    logging.info(wavefront_client)

    try:
        main()
    finally:
        # If the application failed to send metrics/histograms/tracing-spans,
        # you can get the total failure count as follows:
        total_failures = wavefront_client.get_failure_count()
        logging.info(total_failures)

        # On-demand buffer flush
        wavefront_client.flush_now()

        # Close the sender connection
        wavefront_client.close()
