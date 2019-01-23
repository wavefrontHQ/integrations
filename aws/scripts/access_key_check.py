"""
Send AWS IAM User Access Key's expiration date / age to WF as metrics
"""

import logging
import os
import datetime
import json
import boto3
from botocore.vendored import requests


# The AWS_PROFILES must also exist in your ~/.aws/credentials file
AWS_PROFILES = [] # List of aws profiles, to fetch IAM Users Key Age per profile
PROFILE = ''
MAX_KEY_AGE = 180 # max allowed key age
WAVEFRONT_API_TOKEN = '<wavefront api token>'
WAVEFRONT_URL = '<wavefront url>' # the cluster where the key age metric to be pushed
REPORT_URL = WAVEFRONT_URL + '/report'
WRITE_INFO_LOG = 'true'

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# Convert the incoming WRITE_INFO_LOG string true or false into boolean
if str(WRITE_INFO_LOG) == "true" or str(WRITE_INFO_LOG) == "True":
    WRITE_INFO_LOG = True
else:
    WRITE_INFO_LOG = False


def write_log(log_type, log):
    """
    Write log if the WRITE_INFO_LOG is True,
    which is more useful for debugging
    Error logs are always written
    """
    if log_type == "INFO":
        if WRITE_INFO_LOG:
            LOGGER.info(str(log))
        else:
            pass
    elif log_type == "ERROR":
        LOGGER.error(str(log))


def get_key(iam, user):
    """
    Return all the access keys of the given user
    """
    keys = []
    paginator = iam.get_paginator('list_access_keys')
    for access_key in paginator.paginate(UserName=user['UserName']):
        for key in access_key['AccessKeyMetadata']:
            keys.append(key)
    return keys


def get_key_age(key_creation_date):
    """
    Return the Key Age of the user access key
    """
    now_date = datetime.datetime.now()
    now_date = now_date.replace(tzinfo=None)
    key_creation_date = key_creation_date.replace(tzinfo=None)
    date_diff = now_date - key_creation_date
    key_age = date_diff.days
    return key_age


def send_metric_to_wf(items):
    """
    Sends metric to Wavefront via Direct Ingestion API.
    Example in Wavefront data format:
    aws.iam.accessKey 123 source="AWS" name="abc" key="ZX3Vk" status="Active"
                          profile="profile1"
    """
    for item in items:
        metric_name = "aws.iam.accessKey"
        point = 'source="AWS" name="{}" key="{}" status="{}" ' \
                'profile="{}"'.format(item['UserName'],
                                                  item['AccessKeyId'],
                                                  item['AccessKeyStatus'],
                                                  PROFILE)
        data = ('%s %s %s' % (metric_name, item['KeyAge'], point))
        headers = {
            'Authorization': 'Bearer ' + WAVEFRONT_API_TOKEN,
            'Content-Type': 'text/plain'
        }
        try:
            write_log("INFO", "Sending metric to wavefront : " + str(data))
            res = requests.post(url=REPORT_URL, data=data, headers=headers)
            write_log("INFO", res.status_code)
        except requests.exceptions.RequestException as err:
            write_log("ERROR", "ERROR sending metrics to wavefront \n%s" % err)


def list_users(iam):
    """
    Return all AWS users list
    """
    users = []
    paginator = iam.get_paginator('list_users')
    for user in paginator.paginate():
        users.append(user)
    return users[0]['Users']


def handler():
    """
    Main Handler function
    """
    iam = boto3.client('iam')
    aws_users = list_users(iam)
    items = []
    for user in aws_users:
        keys = get_key(iam, user)
        if keys:
            for key in keys:
                key_age = get_key_age(key['CreateDate'])
                items.append({
                        "UserName": key['UserName'],
                        "KeyAge": key_age,
                        "AccessKeyId": key['AccessKeyId'][-5:],
                        "AccessKeyStatus": key['Status']
                })
    return items


if __name__ == "__main__":
    for PROFILE in AWS_PROFILES:
        # Setup session for all AWS_PROFILES to get all IAM Users key age 
        boto3.setup_default_session(profile_name=PROFILE)
        metric_data = handler()
        send_metric_to_wf(metric_data)
