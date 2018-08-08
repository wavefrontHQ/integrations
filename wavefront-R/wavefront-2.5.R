
# R interface to Wavefront (v0.5, 1/12/16)
#  Compatible with Wavefront release 2.4 (Jan 2016)
# 
#  @author Dev Nag (dev@wavefront.com)
#  @author Salil Deshmukh (salil@wavefront.com)
#
# Load this file with
#  > source("/usr/local/R/wavefront.R") 
# ...or the working directory that you placed this file in.
#
# Example call:
#
#   base <- "https://metrics.wavefront.com"  
#   token <- "<myToken>"  # Find this by going to the gear icon at the top right, then click 'Settings'.
#   latency <- wfquery(base, token, wfnow() - wfhours(2), wfnow(), "ts(requests.latency)", clab="h")
#

# Two required libraries; must be installed first if not already there.
library(rjson)
library(RCurl)
library(httr)

#### Convenience methods for setting epoch times

wfminutes <- function(minutesAgo) {
  return (60 * minutesAgo)
}

wfhours <- function(hoursAgo) {
  return (60 * 60 * hoursAgo)
}

wfdays <- function(daysAgo) {
  return (24 * 60 * 60 * daysAgo)
}

wfweeks <- function(weeksAgo) {
  return (7 * 24 * 60 * 60 * weeksAgo)
}

wfquantize <- function(value, interval) {
  return (value - (value %% interval))
}

wfnow <- function() {
  # Normalizes to last minute boundary
  now <- as.integer(Sys.time()) 
  normalizedTime <- wfquantize(now, 60)
  return (normalizedTime);
}


#### Core methods for querying

# Wrapper for retrieving multiple 'lines' based on different expressions; takes vector of ts expressions, returns list of data frames
#    Each data frame can then be retrieved from the result with "result[[1]]", "result[[2]]", etc.
wfqueryvl <- function(baseUrl, token, startTime, endTime, tsExpressionVec,
 	  clab="b",  
	  csep="#",  
          granularity="m",
          includeObsoleteMetrics =TRUE,
          strict=TRUE,
	  debug=FALSE) {
  return (sapply(tsExpressionVec, function (x) wfquery(baseUrl, token, startTime, endTime, x, clab, csep, granularity, includeObsoleteMetrics, strict, debug)))
}

# For retrieving a single data frame
wfquery <- function(baseUrl, token, startTime, endTime, tsExpression, 
	  clab="b",  
	  csep="#",  
          granularity="m",
          includeObsoleteMetrics =TRUE,
          strict=TRUE,
	  debug=FALSE) {
  # Loads data over a given time period for a given ts expression. May use aggregates, tags, etc. Handles https, missing data, etc.
  # Returns NULL if there is an error.
  # 
  #    baseURL: Should be the protocol/hostname of the server, like "https://metrics.wavefront.com" or your VPC. Do NOT include a trailing slash.
  #    token: Should be the unique token generated for your API calls (in Settings).
  #    startTime: Epoch seconds of the interval start; should be on a minute boundary
  #    endTime: Epoch seconds of the interval end; should be on a minute boundary
  #    tsExpression: A normally-formatted tsExpression, like "ts(requests.latency, tag=datacenter1)"
  #    clab: Column labels for metric/hosts; can be "h" for just hosts, "m" for just metrics, and "b" for both (separated by #).
  #            WARNING: If you have multiple duplicate column names, you will need to use indexes rather than names to retrieve them later.
  #    csep: Column name separator between host/metric (only if both are present)
  #    includeObsoleteMetrics: By default set to TRUE to pull obsolete metrics from Wavefront. Set it to FALSE if you dont want to pull obsolete metrics( data older than 6 months)
  #    strict: By default set to TRUE to not return points outside the query window. Set it to FALSE if you want to return the padded points that are outside the query window
  #    debug: If the call returns unexpected data, set this to TRUE to see what's going on inside.  

  #  TODO: Handle pagination for large queries
  #  TODO: Handle DST time shifts

  #  Note: apply() uses for-loops internally, so using for-loops below doesn't hurt performance 

  # Define the desired timeline; default granularity is m(inutes)
  interval <- 60
  if (granularity == "h") { interval <- 60 * 60 }
  if (granularity == "d") { interval <- 24 * 60 * 60 }

  # Quantize the starting/ending times to match the relevant interval boundaries
  startTime <- wfquantize(startTime, interval)  
  endTime <- wfquantize(endTime, interval)

  timeline <- seq.int(startTime, endTime, interval)
  dataLength = length(timeline)

  # Generate URL and download/parse JSON
  url <- paste(baseUrl,"/chart/api", sep="")
  if (debug) { print(url); }
  
  lst = list(q = tsExpression, g = granularity, n = "Unknown", s = as.character(startTime), e = as.character(endTime), t = token, includeObsoleteMetrics = includeObsoleteMetrics, strict = strict)
  if (debug) { print(lst); }
  
  jsonStr <- content(GET(url, query = lst), as = "text", encoding = "UTF-8")
  if (debug) { print(jsonStr); }

  # If not JSON, print literal exception response to terminal
  document <- tryCatch({ 
     fromJSON(json_str=jsonStr, method='C') 
   }, 
   error = function(x) {
    return(NULL);
  });
  if (is.null(document)) { 
    print(paste("Exception received; original response:", jsonStr));
    return(NA); 
  }
  # Shorter name for the actual data in the response
  dList <- document$timeseries;

  # Predefine list of columns; one column for each query key
  frameList <- vector(mode="list", length=length(dList));
  colList <- vector(mode="list", length=length(dList));

  # Process the per-column data for each query key
  for (keyIndex in 1:length(dList)) {
     frameList[[keyIndex]] <- rep(NA, dataLength);       # Start with NA's by default, and overwrite

     # Now, fill in the data, matching by time, leaving all other cells in their current NA state
     rawColData <- dList[[keyIndex]]$data;       

     if ((clab == "m") || (is.null(dList[[keyIndex]]$host))) { 
       # If metric-only was desired, or if host doesn't even exist     
       colList[[keyIndex]] <- dList[[keyIndex]]$label;
     } else if (clab == "h") {
       # If host exists and was desired
       colList[[keyIndex]] <- dList[[keyIndex]]$host; 
     } else { # default
       colList[[keyIndex]] <- paste(dList[[keyIndex]]$label, dList[[keyIndex]]$host, sep=csep);
     }

     if (length(rawColData) > 0) {
       for (timeIndex in seq_along(rawColData)) {
         externalTimeIndex <- (rawColData[[timeIndex]][[1]] - startTime)/interval;
         if ((externalTimeIndex >= 0) & (externalTimeIndex < (dataLength))) {
           frameList[[keyIndex]][externalTimeIndex + 1] <- rawColData[[timeIndex]][[2]];
         } # else, ignore -- point was before/after the desired frame
       }
     }
  }

  # Instantiate data.frame and return
  dFrame <- data.frame(timeline, frameList);
  colnames(dFrame) <- c("time", colList);
  return (dFrame);
}
