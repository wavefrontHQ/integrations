import urllib2
import json
import argparse


def main(servers):
    metrics = []
    for i in range(len(servers)):
        server = servers[i]
        url = "{}/metrics".format(server)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        metrics_to_append = parse_metrics(data)
        for m in metrics_to_append:
            metrics.append(m)

    print(json.dumps(metrics, ensure_ascii=False))


def parse_metrics(all_metrics):
    metrics_to_return = []

    for item in all_metrics:
        metrics_list = item.get("metrics")

        if item.get("type") == "server":
            metrics = {}
            prefix = item.get("id")
            prefix = prefix[5:]
            for m in metrics_list:
                name = "{}.{}".format(prefix, m.get("name"))
                val = m.get("value")
                if val is not None:
                    metrics[name] = val
                else:
                    for key in m:
                        if key != "name":
                            metric_name = "{}.{}".format(name, key)
                            metrics[metric_name] = m[key]
            metrics_to_return.append(metrics)

        if item.get("type") == "tablet":
            tablets = {}
            tag = item.get("attributes").get("table_name")
            tablets["tablet"] = tag
            prefix = "master.tablets"
            for m in metrics_list:
                name = "{}.{}".format(prefix, m.get("name"))
                val = m.get("value")
                if val is not None:
                    tablets[name] = val
                else:
                    for key in m:
                        if key != "name":
                            metric_name = "{}.{}".format(name, key)
                            tablets[metric_name] = m[key]
            metrics_to_return.append(tablets)

    return metrics_to_return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str, nargs='*', help='Kudu Tablet Server or Master address')

    args = parser.parse_args()

    if args.server:
        main(args.server)
    else:
        parser.error('Must specify at least one server address')
