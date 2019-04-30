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

import com.wavefront.rest.models.Dashboard;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import java.io.IOException;

/**
 * A dashboard definition belonging to a particular integration
 */
@ApiModel(description = "A dashboard definition belonging to a particular integration")
@javax.annotation.Generated(value = "io.swagger.codegen.languages.JavaClientCodegen", date = "2019-02-25T16:34:08.557+05:30")
public class IntegrationDashboard {
  @SerializedName("description")
  private String description = null;

  @SerializedName("url")
  private String url = null;

  @SerializedName("dashboardObj")
  private Dashboard dashboardObj = null;

  @SerializedName("name")
  private String name = null;

  public IntegrationDashboard description(String description) {
    this.description = description;
    return this;
  }

  /**
   * Dashboard description
   *
   * @return description
   **/
  @ApiModelProperty(required = true, value = "Dashboard description")
  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public IntegrationDashboard url(String url) {
    this.url = url;
    return this;
  }

  /**
   * URL path to the JSON definition of this dashboard
   *
   * @return url
   **/
  @ApiModelProperty(required = true, value = "URL path to the JSON definition of this dashboard")
  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public IntegrationDashboard dashboardObj(Dashboard dashboardObj) {
    this.dashboardObj = dashboardObj;
    return this;
  }

  /**
   * Get dashboardObj
   *
   * @return dashboardObj
   **/
  @ApiModelProperty(value = "")
  public Dashboard getDashboardObj() {
    return dashboardObj;
  }

  public void setDashboardObj(Dashboard dashboardObj) {
    this.dashboardObj = dashboardObj;
  }

  public IntegrationDashboard name(String name) {
    this.name = name;
    return this;
  }

  /**
   * Dashboard name
   *
   * @return name
   **/
  @ApiModelProperty(required = true, value = "Dashboard name")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    IntegrationDashboard integrationDashboard = (IntegrationDashboard) o;
    return Objects.equals(this.description, integrationDashboard.description) &&
        Objects.equals(this.url, integrationDashboard.url) &&
        Objects.equals(this.dashboardObj, integrationDashboard.dashboardObj) &&
        Objects.equals(this.name, integrationDashboard.name);
  }

  @Override
  public int hashCode() {
    return Objects.hash(description, url, dashboardObj, name);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class IntegrationDashboard {\n");

    sb.append("    description: ").append(toIndentedString(description)).append("\n");
    sb.append("    url: ").append(toIndentedString(url)).append("\n");
    sb.append("    dashboardObj: ").append(toIndentedString(dashboardObj)).append("\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
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

