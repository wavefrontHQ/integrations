import os
import boto3
import json
from botocore.vendored import requests

def handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    res = {}
    for sub in message.split('\n'):
      if '=' in sub:
          #removing single quote from our input
          g1 = [x.strip("'") for x in sub.split('=',1)]
          res[g1[0]]=g1[1];

    name=res['StackName'];
    resource_status= res['ResourceStatus'];
    namespace=res['Namespace'];
    resourceType=res['ResourceType']

    if resource_status == 'CREATE_COMPLETE' and resourceType=='AWS::IAM::Role':
      print('getting stack information');
      client = boto3.client('cloudformation');
      response = client.describe_stacks(StackName = name);
      # parse 
      parameter_array=response['Stacks'][0]['Parameters'];
      #iterate list for set of parameters
      bucketName="";
      rolearn="";
      prefix="";
      accountid="";
      region="";
      externalid="";
      namespaces="";
      secretname="";
      hostname="";
      for item in parameter_array:
          if item['ParameterKey']=='BucketName':
            bucketName=item['ParameterValue'];
          elif item['ParameterKey']=='ExternalId':
            externalid=item['ParameterValue'];
          elif item['ParameterKey']=='Prefix':
            prefix=item['ParameterValue'];                      
          elif item['ParameterKey']=='IAMRoleName':
            rolearn=item['ParameterValue'];                      
          elif item['ParameterKey']=='WavefrontAWSAccountId':
            accountid=item['ParameterValue'];                      
          elif item['ParameterKey']=='Region':
            region=item['ParameterValue'];                      
          elif item['ParameterKey']=='Namespace':
            namespaces=item['ParameterValue'];                     
          elif item['ParameterKey']=='SecretName':
            secretname=item['ParameterValue'];
          elif item['ParameterKey']=='Hostname':
            hostname=item['ParameterValue'];

      roleARN= "arn:aws:iam::"+namespace+":role/"+rolearn;
      print('Sending request to cluster');
      #make http call to cluster

      data={"roleArn":roleARN,"externalId":externalid}
      
      headers = {
      "Authorization": getSecret(secretname),
      "Content-Type": "application/json"
                  }
      #send req to create awsmetric+ and cloudwatch
      url_all= hostname+"/api/external/all?name=AWS";
      resp_all= requests.post(url_all,headers=headers, data=json.dumps(data));
      print("output for Cloudwatch and AWSmetric+ creation");
      print(resp_all);
      id=getId(hostname,headers,roleARN, secretname);
      

      #if bucket non empty, create cloudtrail also
      if bucketName!="" and prefix=="":
          cloudtrail_data= {"name": "cloudtrail integration","service": "cloudTrail","cloudTrail": {"prefix":"","region": "us-west-2","baseCredentials": {"externalId": externalid,"roleArn": roleARN},"bucketName":bucketName}}
      elif bucketName!="" and prefix!="":
          cloudtrail_data= {"name": "cloudtrail integration","service": "cloudTrail","cloudTrail": {"prefix":prefix,"region": "us-west-2","baseCredentials": {"externalId": externalid,"roleArn": roleARN},"bucketName":bucketName}}

      if bucketName!="":
        API_URL=hostname+"/api/v2/cloudintegration";
        r = requests.post(API_URL, headers=headers, data=json.dumps(cloudtrail_data));
        print(r.content);
      
      #UPDATE based on namespaces
      if namespaces!="":
        #make call for put request in AWS cloudwatch
        print("calling namespace update");
        url_namespace= hostname+"/api/v2/cloudintegration/"+id;
        cloudwatchNamespaceData= {"name": "cloudwatch integration","service": "CLOUDWATCH","cloudWatch": {"baseCredentials": {"externalId": externalid ,"roleArn": roleARN},"namespaces": []}}
        splitstring=namespaces.split(",");
        for val in splitstring:
          if val=='Backup' or val== 'Glue' or val=='WAF':
            cloudwatchNamespaceData['cloudWatch']['namespaces'].append(val)
          else:
            value='AWS/'+val;
            cloudwatchNamespaceData['cloudWatch']['namespaces'].append(value);
        responseNamespace= requests.put(url_namespace,headers=headers,data=json.dumps(cloudwatchNamespaceData));

def getId(hostname, headers,roleArn, secretname):
    url_to_get_id= hostname+ "/api/v2/cloudintegration";
    response= requests.get(url_to_get_id,headers=headers);
    jsonResponse = response.json();
    jsonArray=jsonResponse['response']['items']
    id="";
    for jsons in jsonArray:
        if jsons['service'].lower()=='cloudwatch':
            cred=jsons['cloudWatch']['baseCredentials'];
            if cred['roleArn']==roleArn:
                id=jsons['id'];
                break;
    return id;

def getSecret(secretname):
  secrets = boto3.client("secretsmanager");
  apiToken = secrets.get_secret_value(SecretId=secretname);
  print("getting secret");
  tokenJson=json.loads(apiToken['SecretString']);
  return tokenJson['token'];
