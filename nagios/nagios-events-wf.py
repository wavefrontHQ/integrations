#!/usr/bin/python

import argparse
import json
import sys
import requests


def doMain():
    msg = args.msg[0].replace("\\n", "\r").rstrip()
    annotations = {'severity': args.type[0],
                   'type': 'Nagios',
                   'details': msg}

    notif = {'startTime': args.time[0],
             'endTime': args.time[0] + 1,
             'hosts': args.host,
             'annotations': annotations}
    if args.S is not None:
        notif['name'] = "Nagios event on '{}' at '{}'".format(args.service, args.host[0])
    else:
        notif['name'] = "Nagios event at '{}'".format(args.host[0])

    url = "{}/api/v2/event".format(args.server[0])

    headers = {'Content-Type': 'application/json',
               'Content-Encoding': 'gzip',
               'Authorization': 'Bearer ' + args.token[0]}
    result = requests.post(url,
                           headers=headers,
                           data=json.dumps(notif))

    if result.status_code != 200:
        print(result.json())
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

