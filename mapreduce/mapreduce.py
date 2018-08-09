import argparse
import urllib2
import json
import datetime
import sys

def doMain():
    url = '%s/ws/v1/cluster/apps/' % args.server
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e :
       handle_error( "HTTPError " + str(e))
    except urllib2.URLError as e:
        handle_error( "URLError " + str(e))
    except httplib.HTTPException as e:
        handle_error( "HTTPException " + str(e))
    except Exception as e :
        handle_error( "Generic Exception " + str(e))
    else:
        data = json.loads(response.read())
        if "apps" in data:
            apps = []
            for app in data["apps"]["app"]:
                if valid(int(app["finishedTime"]/1000.0)) :
                    apps.append(app)
            print(json.dumps(apps, ensure_ascii=False))

def valid(finishedTime):
    seconds = (datetime.datetime.now() - datetime.datetime.fromtimestamp(finishedTime)).seconds
    if (finishedTime != 0) and (seconds >= 300):
        return False
    return True

def handle_error(error_message):
    sys.stderr.write("ERROR:|MapReduce| " + error_message)
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str, nargs='?', help='ResourceManager Server URL')
    parser.add_argument('--username', type=str, nargs='?', help='ResourceManager Server user.')
    parser.add_argument('--password', type=str, nargs='?', help='ResourceManager Server password.')

    args = parser.parse_args()

    if args.username:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, args.server, args.username, args.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    if not args.server:
        parser.error('server must be provided')
    doMain()
