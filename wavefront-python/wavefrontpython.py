import wavefront_api_client as wave_api
from wavefront_api_client.rest import ApiException
import pandas as pd
import time


#### Convenience methods for setting epoch times

def wfminutes(minutesAgo):
    return (60 * minutesAgo)

def wfhours(hoursAgo):
    return (60 * 60 * hoursAgo)

def wfdays(daysAgo):
    return (24 * 60 * 60 * daysAgo)

def wfweeks(weeksAgo):
    return (7 * 24 * 60 * 60 * weeksAgo)

def wfquantize(value, interval):
    return (value - (value % interval))

def wfnow():
    # Normalizes to last minute boundary
    now = time.time()
    normalizedTime = wfquantize(now, 60)
    return normalizedTime

def get_wfclient(base_url, api_key):
    # Returns Wavefront client object
    config = wave_api.Configuration()
    config.host = base_url
    client = wave_api.ApiClient(configuration=config, header_name='Authorization', header_value='Bearer ' + api_key)
    return client

def get_api_instance(client):
    # Returns Wavefront API's QueryAPI object
    return wave_api.QueryApi(client)

#### Core methods for querying

# Wrapper for retrieving multiple 'lines' based on different expressions; takes list of ts expressions, returns list of data frames
#    Each data frame can then be retrieved from the result with "result[[1]]", "result[[2]]", etc.
def wfqueryvl(base_url, token, start, end, ts_query_vl, granularity,
             strict=True, obsolete_metrics=True):
    dfList = []
    for query in ts_query_vl:
        dfList.append(wfquery(base_url, token, start, end, query, granularity, strict=True, obsolete_metrics=True))
    return dfList

# For retrieving a single data frame
def wfquery(base_url, token, start, end, ts_query, granularity,
             strict=True, obsolete_metrics=True):
    interval = 60
    api_response = None
    dataFrame = pd.DataFrame({})

    if (granularity == "h"):
        interval = 60 * 60
    if (granularity == "d"):
        interval = 24 * 60 * 60

    # Quantize the starting/ending times to match the relevant interval boundaries
    start_time = wfquantize(start, interval)
    end_time = wfquantize(end, interval)

    timeline = range(int(start_time), int(end_time) + interval, interval)
    dataLength = len(timeline)
    tlset = set(timeline)

    try:
        client = get_wfclient(base_url, token)
        api_instance = get_api_instance(client)
        api_response = api_instance.query_api(ts_query, str(start_time), granularity, e=str(end_time))
    except ApiException as e:
        print("Exception when calling QueryApi: %s\n" % e)
        return

    try:
        if api_response.timeseries:
            dList = api_response.timeseries
            for keyIndex in range(0, len(dList)):
                rowColData = dList[keyIndex].data
                if len(rowColData) > 0:
                    if dList[keyIndex].host:
                            colName = dList[keyIndex].host
                    else:
                            colName = dList[keyIndex].label
                    tskey = [row[0] for row in rowColData]
                    tsval = [row[1] for row in rowColData]
                    tskey_match = [i for i, tsd in enumerate(tskey) if tsd in tlset]
                    addHost = pd.DataFrame({colName: [tsval[i] for i in tskey_match]})
                    dataFrame = pd.concat([dataFrame, addHost], axis=1)
            df = pd.DataFrame({'time': timeline})
            dataFrame = pd.concat([df, dataFrame], axis=1)
            return dataFrame
    except (Exception, e):
        print("Exception: {}".format(str(e)))