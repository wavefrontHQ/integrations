import requests
import json
import argparse
import sys


def main(servers):
    metrics = {}
    for i in range(len(servers)):
        try:
            server = servers[i]
            url = "{}/metrics?json".format(server)
            response = requests.get(url)
            data = response.json()
            # impalad or statestored or catalogd
            prefix = data.get("__common__").get("process-name")
            # skip if process is unknown
            if prefix:
                metrics.update(parse_metrics(data.get("metric_group"), prefix))
        except requests.exceptions.InvalidSchema as e:
            handle_error(
                "Verify server URL. Ensure http or https is specified.")
        except requests.exceptions.ConnectionError as e:
            handle_error(
                "Cannot connect to this server URL: '{}'".format(server))
        except Exception as e:
            handle_error("Exception " + str(e))

    if not metrics:
        handle_error("No metrics available")
    print(json.dumps(metrics, ensure_ascii=False))


def parse_metrics(all_metrics, prefix):
    metrics = {}

    for key in all_metrics:
        list = all_metrics.get(key)

        if key == "metrics":
            for l in list:
                name = l.get("name")
                # skip if metric has no name
                if name:
                    # remove extra 'impala' in metric name
                    if name.startswith("impala."):
                        name = name[7:]
                    name = "{}.{}".format(prefix, name)
                    if l.get("kind") == "HISTOGRAM":
                        if l.get("25th %-ile"):
                            metrics["{}.P25".format(name)] = l.get(
                                "25th %-ile")
                        if l.get("50th %-ile"):
                            metrics["{}.P50".format(name)] = l.get(
                                "50th %-ile")
                        if l.get("75th %-ile"):
                            metrics["{}.P75".format(name)] = l.get(
                                "75th %-ile")
                        if l.get("90th %-ile"):
                            metrics["{}.P90".format(name)] = l.get(
                                "90th %-ile")
                        if l.get("95th %-ile"):
                            metrics["{}.P95".format(name)] = l.get(
                                "95th %-ile")
                        if l.get("99.9th %-ile"):
                            metrics["{}.P999".format(name)] = l.get(
                                "99.9th %-ile")
                        if l.get("min"):
                            metrics["{}.min".format(name)] = l.get("min")
                        if l.get("max"):
                            metrics["{}.max".format(name)] = l.get("max")
                        if l.get("count"):
                            metrics["{}.count".format(name)] = l.get("count")
                    elif l.get("last") is not None:
                        val = l.get("last")
                        if isinstance(val, (int, float)):
                            metrics[name] = val
                    elif l.get("value") is not None:
                        val = l.get("value")
                        if isinstance(val, (int, float)):
                            metrics[name] = val
                        elif val == "true":
                            metrics[name] = 1
                        elif val == "false":
                            metrics[name] = 0

        if key == "child_groups":
            for l in list:
                items = l.get("metrics")
                for item in items:
                    name = item.get("name")
                    # skip if metric has no name
                    if name:
                        # remove extra 'impala' in metric name
                        if name.startswith("impala."):
                            name = name[7:]
                        name = "{}.{}".format(prefix, name)
                        if item.get("kind") == "HISTOGRAM":
                            if item.get("25th %-ile"):
                                metrics["{}.P25".format(name)] = item.get(
                                    "25th %-ile")
                            if item.get("50th %-ile"):
                                metrics["{}.P50".format(name)] = item.get(
                                    "50th %-ile")
                            if item.get("75th %-ile"):
                                metrics["{}.P75".format(name)] = item.get(
                                    "75th %-ile")
                            if item.get("90th %-ile"):
                                metrics["{}.P90".format(name)] = item.get(
                                    "90th %-ile")
                            if item.get("95th %-ile"):
                                metrics["{}.P95".format(name)] = item.get(
                                    "95th %-ile")
                            if item.get("99.9th %-ile"):
                                metrics["{}.P999".format(name)] = item.get(
                                    "99.9th %-ile")
                            if item.get("min"):
                                metrics["{}.min".format(
                                    name)] = item.get("min")
                            if item.get("max"):
                                metrics["{}.max".format(
                                    name)] = item.get("max")
                            if item.get("count"):
                                metrics["{}.count".format(name)] = item.get(
                                    "count")
                        elif l.get("last") is not None:
                            val = l.get("last")
                            if isinstance(val, (int, float)):
                                metrics[name] = val
                        elif item.get("value") is not None:
                            val = item.get("value")
                            if isinstance(val, (int, float)):
                                metrics[name] = val
                            elif val == "true":
                                metrics[name] = 1
                            elif val == "false":
                                metrics[name] = 0

    return metrics


def handle_error(msg):
    sys.stderr.write("ERROR|" + msg)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'server',
        type=str,
        nargs='*',
        help='Impala Daemon host address or Impala Statestore host address or \
        Impala Catalog Server host address')

    args = parser.parse_args()

    if args.server:
        main(args.server)
    else:
        parser.error('Must specify at least one server address')
