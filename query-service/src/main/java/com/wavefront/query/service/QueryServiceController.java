package com.wavefront.query.service;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.time.Instant;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.wavefront.rest.api.ApiClient;
import com.wavefront.rest.api.ApiResponse;
import com.wavefront.rest.api.client.QueryApi;
import com.wavefront.rest.models.QueryResult;
import com.wavefront.rest.models.Timeseries;

/**
 * Wavefront Query Service App
 *
 * REST API to execute ts() queries that returns boolean values.
 **/
@RestController
public class QueryServiceController {
  private final Logger log = LoggerFactory.getLogger(
      QueryServiceController.class);

  @RequestMapping("/")
  public String index() {
    return "Query Service is Running!!\n\n" +
        "Usage: /api/v1/query?c=cluster_name&q=ts() with Authorization";
  }

  /**
   * @param authHeader  Wavefront API token to authorise
   * @param clusterName Wavefront cluster name
   * @param query       ts() query which returns boolean value
   * @return  HttpStatus OK - query returns 1;
   * NOT_FOUND - query returns 0;
   * BAD_REQUEST - not a boolean result from query;
   * INTERNAL_SERVER_ERROR - error executing query
   */
  @GetMapping(path = "/api/v1/query", produces = "application/json")
  ResponseEntity<String> execute(
      @RequestHeader(name = "Authorization",
          required = true) String authHeader,
      @RequestParam(name = "c", required = true) String clusterName,
      @RequestParam(name = "q", required = true) String query) {
    try {
      log.debug("Query page");
      ApiClient apiClient = new ApiClient();
      apiClient.setBasePath("https://" + clusterName + ".wavefront.com");
      apiClient.setApiKey(authHeader);
      QueryApi apiq = new QueryApi(apiClient);
      Instant instant = Instant.now();
      long timeStampMillis = instant.toEpochMilli() - 300000;
      ApiResponse<QueryResult> result = apiq.queryApiWithHttpInfo(
          query, Long.toString(timeStampMillis), "m", null, null, null, false,
          false, null, false, false, false, false, false);
      if (result.getStatusCode() == HttpStatus.OK.value()) {
        QueryResult qr = result.getData();
        List<Timeseries> ts = qr.getTimeseries();
        Timeseries t = ts.get(ts.size() - 1);
        List<List<Float>> f = t.getData();
        List<Float> l = f.get(f.size() - 1);
        int lastValue = l.get(1).intValue();
        log.debug("Query executed successfully " + query + " : " + lastValue);
        if (lastValue == 1) {
          return new ResponseEntity<String>(HttpStatus.OK.toString(), null,
              HttpStatus.OK);
        } else if (lastValue == 0) {
          return new ResponseEntity<String>(HttpStatus.NOT_FOUND.toString(),
              null, HttpStatus.NOT_FOUND);
        } else {
          log.warn("Warning: Not a boolean result query: " + query +
              " : " + HttpStatus.BAD_REQUEST);
          return new ResponseEntity<String>(HttpStatus.BAD_REQUEST.toString() +
              " - Warning: Not a boolean result query: " + query,
              null, HttpStatus.BAD_REQUEST);
        }
      } else {
        log.error("Error executing query " + query + " : " +
            HttpStatus.INTERNAL_SERVER_ERROR);
        return new ResponseEntity<String>(
            HttpStatus.INTERNAL_SERVER_ERROR.toString(), null,
            HttpStatus.INTERNAL_SERVER_ERROR);
      }
    } catch (Exception ex) {
      StringWriter sw = new StringWriter();
      ex.printStackTrace(new PrintWriter(sw));
      log.error(sw.toString());
      return new ResponseEntity<String>("Error: While executing the query: " +
          query + " " + ex.getMessage(),
          null,
          HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }
}