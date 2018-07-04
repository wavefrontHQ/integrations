import sys
import requests
import json
import argparse
import time

parser = argparse.ArgumentParser(description='Collects monitoring data from Pingdom.')
parser.add_argument('-u', '--pingdom-user-name', help='The Pingdom User Name', required=True)
parser.add_argument('-p', '--pingdom-password', help='The Pingdom Password', required=True)
parser.add_argument('-a', '--pingdom-api-key', help='The Pingdom API-KEY', required=True)

class Pingdom:
    def __init__(self, api_key, user_name, password):
        self.api_key = api_key,
        self.user_name = user_name,
        self.password = password,
        self.jsonData = []

    def handle_error(self, error_message):
        sys.stderr.write("ERROR:|Pingdom| " + error_message)
        sys.exit(1)

    def call_api(self, api):
        headers = {'App-Key': self.api_key[0]}
        base_api = 'https://api.pingdom.com/api/2.0/' + api
        response = requests.get(base_api, headers=headers, auth=requests.auth.HTTPBasicAuth(self.user_name[0], self.password[0]))

        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error("API [" + base_api + "] failed to execute with error code [" + str(response.status_code) + "].")

    def get_checks(self):
        response = self.call_api('checks')

        data = response.get("checks")
        counts = response.get("counts")
        up_count = 0
        down_count = 0
        unconfirmed_down_count = 0
        unknown_count = 0
        paused_count = 0

        for x in data:
            status = x.get("status")
            if status == "up":
                up_count = up_count + 1
            elif status == "down":
                down_count == down_count + 1
            elif status == "unconfirmed_down":
                unconfirmed_down_count = unconfirmed_down_count + 1
            elif status == "unknown":
                unknown_count = unknown_count + 1
            elif status == "paused":
                paused_count = paused_count + 1

        counts["up"] = up_count
        counts["down"] = down_count
        counts["unconfirmed_down"] = unconfirmed_down_count
        counts["unknown"] = unknown_count
        counts["paused"] = paused_count

        data.append(counts)

        self.jsonData = data

    def get_credits(self):
        response = self.call_api('credits')
        self.jsonData.append(response)

    def get_maintenance(self):
        response = self.call_api('maintenance')

        if response.get('maintenance'):
            for mw in response.get('maintenance'):
                window = {}
                window["description"] = mw.get("description")
                window["recurrencetype"] = mw.get("recurrencetype")
                window["repeatevery"] = mw.get("repeatevery")
                window["from"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mw.get("from")))
                window["to"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mw.get("to")))
                window["window"] = 1

                self.jsonData.append(window)

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        pingdom = Pingdom(args.pingdom_api_key, args.pingdom_user_name, args.pingdom_password)
        pingdom.get_checks()
        pingdom.get_credits()
        pingdom.get_maintenance()
        print(json.dumps(pingdom.jsonData))

    except Exception as e:
        pingdom.handle_error(e.message)
