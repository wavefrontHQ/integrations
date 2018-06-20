import os
import argparse
import json
import sys
import requests
import io
from datetime import datetime, timedelta
     
runscope_service_url = "https://api.runscope.com/buckets"
cache_expiry_min = 60
cache_file = "test_meta_info.txt"

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def cache_test_meta_info(test_meta_info):
    try : 
        with io.open(cache_file, 'w', encoding='utf-8') as outfile:
           str_ = json.dumps(test_meta_info,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
           outfile.write(to_unicode(str_))
           outfile.close()
    except Exception as e:
        handle_error("error writing to cache: " + str(e))

def is_cache_stale():
    if os.path.exists(cache_file):
       file_mod_time = datetime.fromtimestamp(os.stat(cache_file).st_mtime)
       now = datetime.today()
       max_cache_time = timedelta(minutes=cache_expiry_min)
       if now-file_mod_time < max_cache_time:
          return False
    return True
   
def get_cached_test_meta_info():
    try :
        with open(cache_file) as test_mi:
            if test_mi is None:
                return None
            else:
                mi = json.load(test_mi)
                test_mi.close()
                return mi
    except ValueError as ve:
        return None
    except Exception as e:
        handle_error("error reading from cache: " + str(e))

def handle_error(error_message):
    sys.stderr.write("ERROR:|Runscope| " + error_message)
    sys.exit(1)
    
def get_runscope_api_response(url):
    try :
        headers = {}
        headers["Authorization"] = "Bearer {} ".format(args.token[0])
        headers["Content-type"] = "application/json"
        headers["Accept"] = "application/json"
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            em = "error connecting to runscope {}".format(response.status_code)
            handle_error(em)       
    except Exception as e:
        handle_error("error while conneecting to runscope: " + str(e))        

def get_test_bucket_details():
    test_bucket_details = []
    response = get_runscope_api_response(runscope_service_url)
    for data in response['data']:
        test_bucket_meta_info = {}
        test_bucket_meta_info['bucket_name'] = data['name']
        test_bucket_meta_info['tests_url'] = data['tests_url']
        test_bucket_details.append(test_bucket_meta_info)
    return test_bucket_details

def get_test_details(test_bucket_list):
    test_details = []
    for bucket in test_bucket_list:
        response = get_runscope_api_response(bucket['tests_url'])
        for test in response['data']:
            test_meta_info = {}
            test_meta_info['latest_result_url'] = bucket['tests_url'] + "/{}/results/latest".format(test['last_run']['test_uuid'])
            test_meta_info['test_name'] = test['name']
            test_meta_info['test_bucket_name'] = bucket['bucket_name']
            test_details.append(test_meta_info)
    return test_details

def get_test_latest_result(test_details):
    uber_result = []
    for test in test_details:
        response = get_runscope_api_response(test['latest_result_url'])
        for request in response['data']['requests']:
            service_metric = {}
            service_url = request['url']
            if service_url is not None:
               #Need to check on the tag length         
              # request_result = str(request['result'])
               service_metric['service_url'] = service_url[:240]
               service_metric['request_result'] = request['result']
               service_metric['test_name'] = test['test_name']
               service_metric['test_bucket_name'] = test['test_bucket_name']
               service_metric['region'] = response['data']['region']
               service_metric['method'] =  request['method']
               service_metric['assertions_defined'] = request['assertions_defined']
               service_metric['assertions_failed'] = request['assertions_failed']
               service_metric['assertions_passed'] = request['assertions_passed']
               service_metric['scripts_defined'] = request['scripts_defined']
               service_metric['scripts_failed'] = request['scripts_failed']
               service_metric['scripts_passed'] = request['scripts_passed']
               service_metric['variables_defined'] = request['variables_defined']
               service_metric['variables_failed'] = request['variables_failed']
               service_metric['variables_passed'] = request['variables_passed']
               service_metric['timings_dns_lookup_ms'] = request['timings']['dns_lookup_ms']
               service_metric['timings_dial_ms'] = request['timings']['dial_ms']
               service_metric['timings_send_headers_ms'] = request['timings']['send_headers_ms']
               service_metric['timings_send_body_ms'] = request['timings']['send_body_ms']
               service_metric['timings_wait_for_response_ms'] = request['timings']['wait_for_response_ms']
               service_metric['timings_receive_response_ms'] = request['timings']['receive_response_ms']
               uber_result.append(service_metric) 
    if len(uber_result) > 0:
        return uber_result
    else:
        return None

def doMain():
    result = {} 
    if is_cache_stale():
        data_to_cache = get_test_details(get_test_bucket_details())
        cache_test_meta_info(data_to_cache)
        result = get_test_latest_result(data_to_cache)
    else:
        ctm = get_cached_test_meta_info()
        if ctm is None:
            ctm = get_test_details(get_test_bucket_details())
            cache_test_meta_info(ctm)
        result = get_test_latest_result(ctm)

    if result is None:
        handle_error("Empty metric result")
    else:
        str_ = json.dumps(result,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        print(str_)       

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('token', type=str, nargs=1, help='Runscope token.')
	args = parser.parse_args()
doMain()

