/*
 * Wavefront REST API
 * <p>The Wavefront REST API enables you to interact with Wavefront servers using standard REST API tools. You can use the REST API to automate commonly executed operations such as automatically tagging sources.</p><p>When you make REST API calls outside the Wavefront REST API documentation you must add the header \"Authorization: Bearer &lt;&lt;API-TOKEN&gt;&gt;\" to your HTTP requests.</p>
 *
 * OpenAPI spec version: v2
 *
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */


package com.wavefront.rest.models;

import java.util.Objects;

import com.google.gson.TypeAdapter;
import com.google.gson.annotations.JsonAdapter;
import com.google.gson.annotations.SerializedName;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

import com.wavefront.rest.models.ResponseStatus;
import com.wavefront.rest.models.TagsResponse;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import java.io.IOException;

/**
 * JSON container for the HTTP response along with status
 */
@ApiModel(description = "JSON container for the HTTP response along with status")
@javax.annotation.Generated(value = "io.swagger.codegen.languages.JavaClientCodegen", date = "2019-02-25T16:34:08.557+05:30")
public class ResponseContainerTagsResponse {
  @SerializedName("status")
  private ResponseStatus status = null;

  @SerializedName("response")
  private TagsResponse response = null;

  public ResponseContainerTagsResponse status(ResponseStatus status) {
    this.status = status;
    return this;
  }

  /**
   * Get status
   *
   * @return status
   **/
  @ApiModelProperty(required = true, value = "")
  public ResponseStatus getStatus() {
    return status;
  }

  public void setStatus(ResponseStatus status) {
    this.status = status;
  }

  public ResponseContainerTagsResponse response(TagsResponse response) {
    this.response = response;
    return this;
  }

  /**
   * Get response
   *
   * @return response
   **/
  @ApiModelProperty(value = "")
  public TagsResponse getResponse() {
    return response;
  }

  public void setResponse(TagsResponse response) {
    this.response = response;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    ResponseContainerTagsResponse responseContainerTagsResponse = (ResponseContainerTagsResponse) o;
    return Objects.equals(this.status, responseContainerTagsResponse.status) &&
        Objects.equals(this.response, responseContainerTagsResponse.response);
  }

  @Override
  public int hashCode() {
    return Objects.hash(status, response);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ResponseContainerTagsResponse {\n");

    sb.append("    status: ").append(toIndentedString(status)).append("\n");
    sb.append("    response: ").append(toIndentedString(response)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(java.lang.Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

}
