"""System module."""
import json
import boto3
from botocore.vendored import requests


def handler(event, context):
    """Creates a AWS setup."""
    message = event['Records'][0]['Sns']['Message']
    res = {}
    for sub in message.split('\n'):
        if '=' in sub:
            # removing single quote from our input
            data = [x.strip("'") for x in sub.split('=', 1)]
            res[data[0]] = data[1]

    if (
        res['ResourceStatus'] == 'CREATE_COMPLETE'
        and res['ResourceType'] == 'AWS::IAM::Role'
    ):
        # getting stack information
        client = boto3.client('cloudformation')
        response = client.describe_stacks(StackName=res['StackName'])
        # parse
        parameter_array = response['Stacks'][0]['Parameters']
        # iterate list for set of parameters
        parameters = {}
        for item in parameter_array:
            parameters[item['ParameterKey']] = item['ParameterValue']

        bucket_name = parameters.get('BucketName')
        rolearn = parameters.get('IAMRoleName')
        prefix = parameters.get('Prefix')
        region = parameters.get('Region')
        externalid = parameters.get('ExternalId')
        namespaces = parameters.get('Namespace')
        secretname = parameters.get('SecretName')
        hostname = parameters.get('Hostname')

        role_arn = "arn:aws:iam::" + res['Namespace'] + ":role/" + rolearn
        # make http call to cluster
        data = {"roleArn": role_arn, "externalId": externalid}
        headers = {
            "Authorization": gßet_secret(secretname),
            "Content-Type": "application/json"
                        }
        # send req to create awsmetric+ and cloudwatch
        url_all = hostname + "/api/external/all?name=AWS"
        requests.post(url_all, headers=headers, data=json.dumps(data))
        integration_id = get_id(hostname, headers, role_arn)
        # if bucket non empty, create cloudtrail also
        cloudtrail_data = get_request_data(region,
                                        externalid,
                                        role_arn, prefix, bucket_name)
        if bucket_name != "":
            api_url = hostname+"/api/v2/cloudintegration"
            requests.post(api_url,
                        headers=headers,
                        data=json.dumps(cloudtrail_data))

        # update based on namespaces
        if namespaces != "":
            # make call for put request in AWS cloudwatch
            url_namespace = hostname + "/api/v2/cloudintegration/" + integration_id
            namespace_data = {
            "name": "cloudwatch integration",
            "service": "CLOUDWATCH",
            "cloudWatch":
            {
                "baseCredentials":
                {"externalId": externalid,
                "roleArn": role_arn}, "namespaces": []}}
            exclude_value = ['Backup', 'Glue', 'WAF']
            for val in namespaces.split(","):
                if val in exclude_value:
                    namespace_data['cloudWatch']['namespaces'].append(val)
                else:
                    value = 'AWS/'+val
                    namespace_data['cloudWatch']['namespaces'].append(value)
            requests.put(url_namespace,
                        headers=headers,
                        data=json.dumps(namespace_data))


def get_id(hostname, headers, role_arn):
    """Returns the cloudintegration Id."""
    url_to_get_id = hostname + "/api/v2/cloudintegration"
    response = requests.get(url_to_get_id, headers=headers)
    json_response = response.json()
    json_array = json_response['response']['items']
    integration_id = ""
    for jsons in json_array:
        if jsons['service'].lower() == 'cloudwatch':
            cred = jsons['cloudWatch']['baseCredentials']
            if cred['roleArn'] == role_arn:
                integration_id = jsons['id']
                break
    return integration_id


def get_request_data(region, externalid, role_arn, prefix, bucket_name):
    """Returns the cloudtrail request data."""
    cloudtrail_data = ""
    if bucket_name != "" and prefix == "":
        cloudtrail_data = {
          "name": "cloudtrail integration",
          "service": "cloudTrail",
          "cloudTrail":
          {
            "prefix": "",
            "region": region,
            "baseCredentials":
            {"externalId": externalid,
             "roleArn": role_arn},
            "bucketName": bucket_name
          }}
    elif bucket_name != "" and prefix != "":
        cloudtrail_data = {
          "name": "cloudtrail integration",
          "service": "cloudTrail",
          "cloudTrail":
          {
            "prefix": prefix,
            "region": region,
            "baseCredentials":
            {"externalId": externalid,
             "roleArn": role_arn},
            "bucketName": bucket_name
          }}
    return cloudtrail_data


def get_secret(secretname):
    """Get the token for the Wavefront API calls.
    Args: secretname (String)
    Returns: String: token_json['token']"""
    secrets = boto3.client("secretsmanager")
    api_token = secrets.get_secret_value(SecretId=secretname)
    print("getting secret")
    token_json = json.loads(api_token['SecretString'])
    return token_json['token']
