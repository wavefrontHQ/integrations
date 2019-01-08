# Wavefront Python Library

The Wavefront Python library allows you to perform ts() queries in Python to retieve the metrics data in numeric format, as a Python pandas dataframe.

## Usage

  To retieve metric data for a single query

	dataframe = wfquery(serverURL, wavefrontAccountToken, startTime, endTime, query, granularity)

	serverURl : Wavefront cluster/server to query.
	wavefrontAccountToken : API key to authenticate.
	startTime : metrics to be collected from this time, in epoch format.
	endTime : metrics to be collected till this time, in epoch format.
	query : ts() query for which metric data has to be collected.
	granularity : specifies the number of collections within the start and end time.


  To retieve metric data for multiple queries

  	dataset = wfqueryvl(serverURL, wavefrontAccountToken, startTime, endTime, ts_query_vl, granularity)

  	All the parameters are same as above, except `ts_query_vl`. This param is a list of ts() queries which returns a dataset, a list of dataframes corresponding to each query.

Refer to [Visualizing Metrics with Python](https://docs.wavefront.com/integrations_python.html) to learn how to use Python to visualize metrics in Wavefront.
