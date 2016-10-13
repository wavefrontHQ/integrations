
# Usage:
# python t.py -a YOUR_ACCESS_KEY_ID -s YOUR_SECRET_ACCESS_KEY -r YOUR_REGION -A telegraf

import argparse
import requests
import subprocess
import json
import os
import sys

parser = argparse.ArgumentParser(description='Add EC2 Instance Tags to your agent configuration.')
parser.add_argument('-a', '--aws-access-key-id', help='The AWS Access Key ID', required=True)
parser.add_argument('-s', '--aws-secret-access-key', help='The AWS Secret Access Key', required=True)
parser.add_argument('-r', '--aws-default-region', help='The AWS Default Region to use for querying EC2 metadata', required=True)
parser.add_argument('-A', '--agent', help='Agent configuration you wish to modify ("collectd" or "telegraf")', required=True)
parser.add_argument('-t', '--telegraf-config-path', help='Path to Telegraf configuration file', default='/etc/telegraf/telegraf.conf')

def get_instance_id():
    r = requests.get("http://instance-data/latest/meta-data/instance-id")
    return r.content

def set_aws_env_vars(access_key_id, secret_key, default_region):
    try:
        os.environ["AWS_ACCESS_KEY_ID"] = str(access_key_id)
        os.environ["AWS_SECRET_ACCESS_KEY"] = str(secret_key)
        os.environ["AWS_DEFAULT_REGION"] = str(default_region)
    except:
        print "Error setting AWS environment variables:", sys.exc_info()[0]

def tag_telegraf_config(tags, conf_path):
    tags_pre = "BEGIN EC2 TAGS"
    tags_post = "END EC2 TAGS"
    # write tags to tags.txt
    tagStr = "  # %s\n" % (tags_pre)
    for tag in tags:
        tagStr += "\t" + tag + "\n"
    tagStr += "  # %s\n" % (tags_post)
    try:
        tagTxt = open("tags.txt","w")
        tagTxt.write(tagStr)
        tagTxt.close()
    except:
        print "Error writing tags.txt", sys.exc_info()[0]
        sys.exit()

    # remove existing ec2 tags
    conf = conf_path
    cmd = "sudo sed -i '/%s/,/%s/d' %s" % (tags_pre, tags_post, conf)
    #print cmd
    output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

    cmd = "sudo sed -i '/\[global_tags\]/r tags.txt' %s" % (conf_path)
    try:
        output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except:
        print "Error overwriting telegraf.conf. Is the file located at ", conf_path, "? ", sys.exc_info()[0]
        sys.exit()

    cmd = "sudo service telegraf restart"
    try:
        output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except:
        "Error restarting telegraf:", sys.exc_info()[0]
        sys.exit()

def get_instance_tags(instance_id):
    # use aws cli to get tags (will return json)
    filter = '--filters "Name=resource-id,Values='+instance_id+'"'
    cmd = "aws ec2 describe-tags " + filter
    #try:
    data = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    #except:
    #    print "Error querying for ec2 instance tags", sys.exc_info()[0]
    #    sys.exit()
    tagjs = json.loads(data)

    output_tags = []
    for tag in tagjs['Tags']:
        name = tag['Key']
        value = tag['Value']
        out_tag = '%s="%s"' % (name,value)
        output_tags.append(out_tag)
    return output_tags

def main():
    args = parser.parse_args()
    set_aws_env_vars(args.aws_access_key_id,args.aws_secret_access_key,args.aws_default_region)
    instance_id = get_instance_id()
    tags = get_instance_tags(instance_id)
    print "Instance %s has %d tags" % (instance_id, len(tags))

    if args.agent == "telegraf":
        print "Adding global tags to configuration file and restarting Telegraf."
        tag_telegraf_config(tags,args.telegraf_config_path)

if __name__ == "__main__":
    main()
