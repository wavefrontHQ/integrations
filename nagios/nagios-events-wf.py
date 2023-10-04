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

    if args.S is not None:
        name = "Nagios event on '{}' at '{}'".format(args.service, args.host)
    else:
        name = "Nagios event at '{}'".format(args.host)

    wavefront_client.send_event(name, startTime, endTime, args.host, ["env:", "test-event"], annotations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', dest="server", help='Wavefront Server URL.')
    parser.add_argument('--token', dest="token", help='Wavefront token.')
    parser.add_argument('-S', action='store_true', help='Service notification.')
    parser.add_argument('--type', help='Notification type.')
    parser.add_argument('--host', help='Notification hostname.')
    parser.add_argument('--service', type=str, nargs='?', help='Notification service name.')
    parser.add_argument('--time', type=int, help='Notification time (UNIX epoch).')
    parser.add_argument('--msg', help='Notification message.')
    parser.add_argument('--wf_proxy_addr', dest="addr")
    parser.add_argument('--wf_proxy_port', dest="port")
    parser.add_argument('--csp_base_url', dest="csp_base_url", help='Base URL of CSP console.')
    parser.add_argument('--csp_api_token', dest="csp_api_token", help='CSP API Token for csp authentication.')
    parser.add_argument('--csp_app_id', dest="csp_app_id", help='CSP OAuth App ID for csp authentication.')
    parser.add_argument('--csp_app_secret', dest="csp_app_secret", help='CSP OAuth App secret for csp authentication.')
    parser.add_argument('--csp_org_id', dest="csp_org_id", help='CSP Organization ID for csp authentication.')

    args = parser.parse_args()
    logging.info(args)
    wavefront_server = None
    
    if args.addr is not None and args.port is not None:
        wavefront_server = "proxy://{}:{}".format(args.addr, args.port)
    elif args.server is not None and args.token is not None:
        wavefront_server = args.server[:8] + args.token + '@' + args.server[8:]
    else:
        wavefront_server = args.server

    csp_base_url, csp_token = None, None
    csp_app_id, csp_app_secret, csp_org_id = None, None, None
    args_length = sum(1 for arg_value in vars(args).values() if arg_value is not None)

    if args.csp_api_token is not None:
        csp_base_url = args.csp_base_url
        csp_token = args.csp_api_token
    elif args.csp_app_id is not None:
        csp_base_url = args.csp_base_url
        csp_app_id = args.csp_app_id
        csp_app_secret = args.csp_app_secret
        if args_length > 5:
            csp_org_id = args.csp_org_id

    client_factory = WavefrontClientFactory()
    client_factory.add_client(url=wavefront_server,
                              csp_base_url=csp_base_url,
                              csp_api_token=csp_token,
                              csp_app_id=csp_app_id,
                              csp_app_secret=csp_app_secret,
                              csp_org_id=csp_org_id)
    wavefront_client = client_factory.get_client()

    try:
        main()
    finally:
        # If the application failed to send metrics/histograms/tracing-spans,
        # you can get the total failure count as follows:
        total_failures = wavefront_client.get_failure_count()

        # On-demand buffer flush
        wavefront_client.flush_now()

        # Close the sender connection
        wavefront_client.close()
