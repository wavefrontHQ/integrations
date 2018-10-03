import requests
import json
import argparse
import sys


def main(servers):
    metrics = []
    for i in range(len(servers)):
        try:
            server = servers[i]
            url = "{}/metrics".format(server)
            response = requests.get(url)
            if not response.raise_for_status():
                data = response.json()
                metrics_to_append = parse_metrics(data)
                metrics.extend(metrics_to_append)
        except requests.exceptions.InvalidSchema as e:
            handle_error(
                "URLError: Verify server URL. Ensure http or https is specified.")
        except requests.exceptions.ConnectionError as e:
            handle_error(
                "ConnectionError: Cannot connect to this server URL: '{}'".format(server))
        except Exception as e:
            handle_error("Exception " + str(e))

    if not metrics:
        raise Exception("No metrics available")
    print(json.dumps(metrics, ensure_ascii=False))


def parse_metrics(all_metrics):
    metrics_to_return = []

    for item in all_metrics:
        metrics_list = item.get("metrics")

        if metrics_list:
            # obtain server (tablet or master) metrics
            if item.get("type") == "server":
                metrics = {}
                # id specifies whether it is a tablet server or master
                # eg. kudu.tabletserver or kudu.master
                prefix = item.get("id")
                # skip if server type is unknown
                if prefix:
                    # Telegraf configuration will add 'kudu' as a prefix
                    prefix = prefix.replace("kudu.", "")
                    for m in metrics_list:
                        # some server metric names contain another 'kudu'
                        name = "{}.{}".format(prefix, m.get("name").
                                              replace("_kudu", ""))
                        val = m.get("value")
                        if val is not None:
                            metrics[name] = val
                        # histogram metrics do not have a 'value' key
                        else:
                            for key in m:
                                if key != "name":
                                    metric_name = "{}.{}".format(name, key)
                                    metrics[metric_name] = m[key]
                    metrics_to_return.append(metrics)

            # obtain tablet metrics
            if item.get("type") == "tablet":
                tablets = {}
                # set table name as a point tag for metrics
                tag = item.get("attributes").get("table_name")
                # skip if table is unknown
                if tag is not None:
                    tablets["table"] = tag
                    # id is not as useful so setting our own prefix
                    prefix = "master.tablets"
                    for m in metrics_list:
                        name = "{}.{}".format(prefix, m.get("name"))
                        val = m.get("value")
                        if val is not None:
                            tablets[name] = val
                        # histogram metrics do not have a 'value' key
                        else:
                            for key in m:
                                if key != "name":
                                    metric_name = "{}.{}".format(name, key)
                                    tablets[metric_name] = m[key]
                    metrics_to_return.append(tablets)

    return metrics_to_return


def handle_error(msg):
    sys.stderr.write("ERROR|" + msg)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str, nargs='*',
                        help='Kudu Tablet Server or Master address')

    args = parser.parse_args()

    if args.server:
        main(args.server)
    else:
        parser.error('Must specify at least one server address')
