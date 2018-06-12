#!/usr/bin/env python
# Usage:
# python convox.py -a convox-api-key

import requests
import json
import argparse

convox = []
rack_list = []
app_list = []
org_list = []

parser = argparse.ArgumentParser(description='Collects monitoring data from convox.')
parser.add_argument('-a', '--convox-api-key', help='The Convox Api Key', required=True)


def set_global_parameters(secret_key):
    global header_dict
    global api_dict
    global api_key
    api_key = secret_key

    header_dict = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}

    api_dict = {"base": "https://console.convox.com/"}


def add_rack_level_tags(metrics_dict, rack):
    metrics_dict["organization"] = rack.get("organization")
    metrics_dict["rack"] = rack.get("rack")


def add_app_level_tags(metrics_dict, app):
    metrics_dict["app"] = app.get("app")
    add_rack_level_tags(metrics_dict, app)


def call_api(api, request_headers):
    base_req = api_dict.get("base") + api
    response = requests.get(base_req, headers=request_headers, auth=requests.auth.HTTPBasicAuth('', api_key))

    if response.status_code == 200:
        return response.json()
    else:
        #print "API [" + base_req + "] failed to execute with error code [" + str(response.status_code) + "]."

        return None


def get_racks():
    call_to = "racks"
    response = call_api(call_to, header_dict)
    if response:
        for data in response:
            mini_convox = {}
            if data.get("status") == "running":
                mini_convox["rack_status"] = 1
            else:
                mini_convox["rack_status"] = 0

            org = data.get("organization").get("name")
            mini_convox["organization"] = org
            mini_convox["rack"] = data.get("name")
            rack_list.append(mini_convox)
            org_list.append(org)
            convox.append(mini_convox)


def get_apps():
    call_to = "apps"
    for rack in rack_list:
        current_header_dict = dict(header_dict)
        current_header_dict["rack"] = rack.get("rack")
        response = call_api(call_to, current_header_dict)
        if response:
            for data in response:
                mini_convox = {}
                if data.get("status") == "running":
                    mini_convox["app_status"] = 1
                else:
                    mini_convox["app_status"] = 0
                if data.get("sleep"):
                    mini_convox["app_sleep"] = 1
                else:
                    mini_convox["app_sleep"] = 0

                mini_convox["app"] = data.get("name")
                add_rack_level_tags(mini_convox, rack)
                app_list.append(mini_convox)
                convox.append(mini_convox)


def get_builds():
    for app in app_list:
        mini_build = {}
        current_header_dict = dict(header_dict)
        current_header_dict["rack"] = app.get("rack")
        call_to = "apps/" + app.get("app") + "/builds"
        all_builds = call_api(call_to, current_header_dict)
        if all_builds:
            for build in all_builds:
                mini_build["id"] = build.get("id")
                mini_build["release"] = build.get("release")
                mini_build["status"] = build.get("status")
                mini_build["started"] = build.get("started")
                mini_build["ended"] = build.get("ended")

                if build.get("status") == "complete":
                    mini_build["app_build_completed"] = 1
                    mini_build["app_build_finished"] = 1
                else:
                    mini_build["app_build_completed"] = 0
                    mini_build["app_build_finished"] = 0

            add_app_level_tags(mini_build, app)
            convox.append(mini_build)


def get_instances():
    call_to = "instances"
    for rack in rack_list:
        current_header_dict = dict(header_dict)
        current_header_dict["rack"] = rack.get("rack")
        response = call_api(call_to, current_header_dict)
        if response:
            for data in call_api(call_to, current_header_dict):
                sub_instance = {}
                sub_instance["rack_instance_cpu"] = data.get("cpu")
                sub_instance["rack_instance_memory"] = data.get("memory")
                sub_instance["rack_instance_processes"] = data.get("processes")
                if data.get("status") == "active":
                    sub_instance["rack_instance_status"] = 1
                else:
                    sub_instance["rack_instance_status"] = 0
                sub_instance["id"] = data.get("id")

                add_rack_level_tags(sub_instance, rack)
                convox.append(sub_instance)


def get_app_formation():
    for app in app_list:
        sub_formation = {}
        call_to = "apps/" + app.get("app") + "/formation"
        current_header_dict = dict(header_dict)
        current_header_dict["rack"] = app.get("rack")
        response = call_api(call_to, current_header_dict)
        if response:
            for data in response:
                sub_formation["app_formation_cpu"] = data.get("cpu")
                sub_formation["app_formation_memory"] = data.get("memory")
                add_app_level_tags(sub_formation, app)
                convox.append(sub_formation)


def get_app_process():
    for app in app_list:
        sub_process = {}
        call_to = "apps/" + app.get("app") + "/processes"
        current_header_dict = dict(header_dict)
        current_header_dict["rack"] = app.get("rack")
        response = call_api(call_to, current_header_dict)
        if response:
            for data in response:
                sub_process["app_process_cpu"] = data.get("cpu")
                sub_process["app_process_memory"] = data.get("memory")
                sub_process["name"] = data.get("name")
                sub_process["id"] = data.get("id")

                add_app_level_tags(sub_process, app)
                convox.append(sub_process)


def get_services():
    call_to = "services"
    response = call_api(call_to, header_dict)
    if response:
        for data in response:
            sub_service = {}
            sub_service["name"] = data.get("name")
            sub_service["type"] = data.get("type")
            if data.get("status") == "running":
                sub_service["service_status"] = 1
            else:
                sub_service["service_status"] = 0

            convox.append(sub_service)


def get_system_capacity():
    call_to = "system/capacity"
    data = call_api(call_to, header_dict)
    system_info = {}
    if data:
        system_info["system_capacity_process_cpu"] = data.get("process-cpu")
        system_info["system_capacity_process_width"] = data.get("process-width")
        system_info["system_capacity_process_count"] = data.get("process-count")
        system_info["system_capacity_process_memory"] = data.get("process-memory")
        system_info["system_capacity_cluster_memory"] = data.get("cluster-memory")
        system_info["system_capacity_cluster_cpu"] = data.get("cluster-cpu")
        system_info["system_capacity_instance_memory"] = data.get("instance-memory")
        system_info["system_capacity_instance_cpu"] = data.get("instance-cpu")

        convox.append(system_info)


def get_organization():
    org_count = {"organization_count": len(set(org_list))}
    convox.append(org_count)


if __name__ == "__main__":
    set_global_parameters(parser.parse_args().convox_api_key)
    get_racks()
    get_apps()
    get_builds()
    get_instances()
    get_app_formation()
    get_app_process()
    get_services()
    get_system_capacity()
    get_organization()

    print json.dumps(convox)
