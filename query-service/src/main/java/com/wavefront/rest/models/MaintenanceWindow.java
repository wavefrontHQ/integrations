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

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Wavefront maintenance window entity
 */
@ApiModel(description = "Wavefront maintenance window entity")
@javax.annotation.Generated(value = "io.swagger.codegen.languages.JavaClientCodegen", date = "2019-02-25T16:34:08.557+05:30")
public class MaintenanceWindow {
  @SerializedName("reason")
  private String reason = null;

  @SerializedName("customerId")
  private String customerId = null;

  @SerializedName("relevantCustomerTags")
  private List<String> relevantCustomerTags = new ArrayList<String>();

  @SerializedName("title")
  private String title = null;

  @SerializedName("startTimeInSeconds")
  private Long startTimeInSeconds = null;

  @SerializedName("endTimeInSeconds")
  private Long endTimeInSeconds = null;

  @SerializedName("relevantHostTags")
  private List<String> relevantHostTags = null;

  @SerializedName("relevantHostNames")
  private List<String> relevantHostNames = null;

  @SerializedName("creatorId")
  private String creatorId = null;

  @SerializedName("updaterId")
  private String updaterId = null;

  @SerializedName("id")
  private String id = null;

  @SerializedName("createdEpochMillis")
  private Long createdEpochMillis = null;

  @SerializedName("updatedEpochMillis")
  private Long updatedEpochMillis = null;

  @SerializedName("relevantHostTagsAnded")
  private Boolean relevantHostTagsAnded = null;

  @SerializedName("hostTagGroupHostNamesGroupAnded")
  private Boolean hostTagGroupHostNamesGroupAnded = null;

  @SerializedName("eventName")
  private String eventName = null;

  /**
   * Gets or Sets runningState
   */
  @JsonAdapter(RunningStateEnum.Adapter.class)
  public enum RunningStateEnum {
    ONGOING("ONGOING"),

    PENDING("PENDING"),

    ENDED("ENDED");

    private String value;

    RunningStateEnum(String value) {
      this.value = value;
    }

    public String getValue() {
      return value;
    }

    @Override
    public String toString() {
      return String.valueOf(value);
    }

    public static RunningStateEnum fromValue(String text) {
      for (RunningStateEnum b : RunningStateEnum.values()) {
        if (String.valueOf(b.value).equals(text)) {
          return b;
        }
      }
      return null;
    }

    public static class Adapter extends TypeAdapter<RunningStateEnum> {
      @Override
      public void write(final JsonWriter jsonWriter, final RunningStateEnum enumeration) throws IOException {
        jsonWriter.value(enumeration.getValue());
      }

      @Override
      public RunningStateEnum read(final JsonReader jsonReader) throws IOException {
        String value = jsonReader.nextString();
        return RunningStateEnum.fromValue(String.valueOf(value));
      }
    }
  }

  @SerializedName("runningState")
  private RunningStateEnum runningState = null;

  @SerializedName("sortAttr")
  private Integer sortAttr = null;

  public MaintenanceWindow reason(String reason) {
    this.reason = reason;
    return this;
  }

  /**
   * The purpose of this maintenance window
   *
   * @return reason
   **/
  @ApiModelProperty(required = true, value = "The purpose of this maintenance window")
  public String getReason() {
    return reason;
  }

  public void setReason(String reason) {
    this.reason = reason;
  }

  /**
   * Get customerId
   *
   * @return customerId
   **/
  @ApiModelProperty(value = "")
  public String getCustomerId() {
    return customerId;
  }

  public MaintenanceWindow relevantCustomerTags(List<String> relevantCustomerTags) {
    this.relevantCustomerTags = relevantCustomerTags;
    return this;
  }

  public MaintenanceWindow addRelevantCustomerTagsItem(String relevantCustomerTagsItem) {
    this.relevantCustomerTags.add(relevantCustomerTagsItem);
    return this;
  }

  /**
   * List of alert tags whose matching alerts will be put into maintenance because of this maintenance window
   *
   * @return relevantCustomerTags
   **/
  @ApiModelProperty(required = true, value = "List of alert tags whose matching alerts will be put into maintenance because of this maintenance window")
  public List<String> getRelevantCustomerTags() {
    return relevantCustomerTags;
  }

  public void setRelevantCustomerTags(List<String> relevantCustomerTags) {
    this.relevantCustomerTags = relevantCustomerTags;
  }

  public MaintenanceWindow title(String title) {
    this.title = title;
    return this;
  }

  /**
   * Title of this maintenance window
   *
   * @return title
   **/
  @ApiModelProperty(required = true, value = "Title of this maintenance window")
  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public MaintenanceWindow startTimeInSeconds(Long startTimeInSeconds) {
    this.startTimeInSeconds = startTimeInSeconds;
    return this;
  }

  /**
   * The time in epoch seconds when this maintenance window will start
   *
   * @return startTimeInSeconds
   **/
  @ApiModelProperty(required = true, value = "The time in epoch seconds when this maintenance window will start")
  public Long getStartTimeInSeconds() {
    return startTimeInSeconds;
  }

  public void setStartTimeInSeconds(Long startTimeInSeconds) {
    this.startTimeInSeconds = startTimeInSeconds;
  }

  public MaintenanceWindow endTimeInSeconds(Long endTimeInSeconds) {
    this.endTimeInSeconds = endTimeInSeconds;
    return this;
  }

  /**
   * The time in epoch seconds when this maintenance window will end
   *
   * @return endTimeInSeconds
   **/
  @ApiModelProperty(required = true, value = "The time in epoch seconds when this maintenance window will end")
  public Long getEndTimeInSeconds() {
    return endTimeInSeconds;
  }

  public void setEndTimeInSeconds(Long endTimeInSeconds) {
    this.endTimeInSeconds = endTimeInSeconds;
  }

  public MaintenanceWindow relevantHostTags(List<String> relevantHostTags) {
    this.relevantHostTags = relevantHostTags;
    return this;
  }

  public MaintenanceWindow addRelevantHostTagsItem(String relevantHostTagsItem) {
    if (this.relevantHostTags == null) {
      this.relevantHostTags = new ArrayList<String>();
    }
    this.relevantHostTags.add(relevantHostTagsItem);
    return this;
  }

  /**
   * List of source/host tags whose matching sources/hosts will be put into maintenance because of this maintenance window
   *
   * @return relevantHostTags
   **/
  @ApiModelProperty(value = "List of source/host tags whose matching sources/hosts will be put into maintenance because of this maintenance window")
  public List<String> getRelevantHostTags() {
    return relevantHostTags;
  }

  public void setRelevantHostTags(List<String> relevantHostTags) {
    this.relevantHostTags = relevantHostTags;
  }

  public MaintenanceWindow relevantHostNames(List<String> relevantHostNames) {
    this.relevantHostNames = relevantHostNames;
    return this;
  }

  public MaintenanceWindow addRelevantHostNamesItem(String relevantHostNamesItem) {
    if (this.relevantHostNames == null) {
      this.relevantHostNames = new ArrayList<String>();
    }
    this.relevantHostNames.add(relevantHostNamesItem);
    return this;
  }

  /**
   * List of source/host names that will be put into maintenance because of this maintenance window
   *
   * @return relevantHostNames
   **/
  @ApiModelProperty(value = "List of source/host names that will be put into maintenance because of this maintenance window")
  public List<String> getRelevantHostNames() {
    return relevantHostNames;
  }

  public void setRelevantHostNames(List<String> relevantHostNames) {
    this.relevantHostNames = relevantHostNames;
  }

  /**
   * Get creatorId
   *
   * @return creatorId
   **/
  @ApiModelProperty(value = "")
  public String getCreatorId() {
    return creatorId;
  }

  /**
   * Get updaterId
   *
   * @return updaterId
   **/
  @ApiModelProperty(value = "")
  public String getUpdaterId() {
    return updaterId;
  }

  public MaintenanceWindow id(String id) {
    this.id = id;
    return this;
  }

  /**
   * Get id
   *
   * @return id
   **/
  @ApiModelProperty(value = "")
  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  /**
   * Get createdEpochMillis
   *
   * @return createdEpochMillis
   **/
  @ApiModelProperty(value = "")
  public Long getCreatedEpochMillis() {
    return createdEpochMillis;
  }

  /**
   * Get updatedEpochMillis
   *
   * @return updatedEpochMillis
   **/
  @ApiModelProperty(value = "")
  public Long getUpdatedEpochMillis() {
    return updatedEpochMillis;
  }

  public MaintenanceWindow relevantHostTagsAnded(Boolean relevantHostTagsAnded) {
    this.relevantHostTagsAnded = relevantHostTagsAnded;
    return this;
  }

  /**
   * Whether to AND source/host tags listed in relevantHostTags. If true, a source/host must contain all tags in order for the maintenance window to apply.  If false, the tags are OR&#39;ed, and a source/host must contain one of the tags. Default: false
   *
   * @return relevantHostTagsAnded
   **/
  @ApiModelProperty(value = "Whether to AND source/host tags listed in relevantHostTags. If true, a source/host must contain all tags in order for the maintenance window to apply.  If false, the tags are OR'ed, and a source/host must contain one of the tags. Default: false")
  public Boolean isRelevantHostTagsAnded() {
    return relevantHostTagsAnded;
  }

  public void setRelevantHostTagsAnded(Boolean relevantHostTagsAnded) {
    this.relevantHostTagsAnded = relevantHostTagsAnded;
  }

  public MaintenanceWindow hostTagGroupHostNamesGroupAnded(Boolean hostTagGroupHostNamesGroupAnded) {
    this.hostTagGroupHostNamesGroupAnded = hostTagGroupHostNamesGroupAnded;
    return this;
  }

  /**
   * If true, a source/host must be in &#39;relevantHostNames&#39; and have tags matching the specification formed by &#39;relevantHostTags&#39; and &#39;relevantHostTagsAnded&#39; in order for this maintenance window to apply. If false, a source/host must either be in &#39;relevantHostNames&#39; or match &#39;relevantHostTags&#39; and &#39;relevantHostTagsAnded&#39;. Default: false
   *
   * @return hostTagGroupHostNamesGroupAnded
   **/
  @ApiModelProperty(value = "If true, a source/host must be in 'relevantHostNames' and have tags matching the specification formed by 'relevantHostTags' and 'relevantHostTagsAnded' in order for this maintenance window to apply. If false, a source/host must either be in 'relevantHostNames' or match 'relevantHostTags' and 'relevantHostTagsAnded'. Default: false")
  public Boolean isHostTagGroupHostNamesGroupAnded() {
    return hostTagGroupHostNamesGroupAnded;
  }

  public void setHostTagGroupHostNamesGroupAnded(Boolean hostTagGroupHostNamesGroupAnded) {
    this.hostTagGroupHostNamesGroupAnded = hostTagGroupHostNamesGroupAnded;
  }

  /**
   * The name of an event associated with the creation/update of this maintenance window
   *
   * @return eventName
   **/
  @ApiModelProperty(value = "The name of an event associated with the creation/update of this maintenance window")
  public String getEventName() {
    return eventName;
  }

  /**
   * Get runningState
   *
   * @return runningState
   **/
  @ApiModelProperty(value = "")
  public RunningStateEnum getRunningState() {
    return runningState;
  }

  /**
   * Numeric value used in default sorting
   *
   * @return sortAttr
   **/
  @ApiModelProperty(value = "Numeric value used in default sorting")
  public Integer getSortAttr() {
    return sortAttr;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    MaintenanceWindow maintenanceWindow = (MaintenanceWindow) o;
    return Objects.equals(this.reason, maintenanceWindow.reason) &&
        Objects.equals(this.customerId, maintenanceWindow.customerId) &&
        Objects.equals(this.relevantCustomerTags, maintenanceWindow.relevantCustomerTags) &&
        Objects.equals(this.title, maintenanceWindow.title) &&
        Objects.equals(this.startTimeInSeconds, maintenanceWindow.startTimeInSeconds) &&
        Objects.equals(this.endTimeInSeconds, maintenanceWindow.endTimeInSeconds) &&
        Objects.equals(this.relevantHostTags, maintenanceWindow.relevantHostTags) &&
        Objects.equals(this.relevantHostNames, maintenanceWindow.relevantHostNames) &&
        Objects.equals(this.creatorId, maintenanceWindow.creatorId) &&
        Objects.equals(this.updaterId, maintenanceWindow.updaterId) &&
        Objects.equals(this.id, maintenanceWindow.id) &&
        Objects.equals(this.createdEpochMillis, maintenanceWindow.createdEpochMillis) &&
        Objects.equals(this.updatedEpochMillis, maintenanceWindow.updatedEpochMillis) &&
        Objects.equals(this.relevantHostTagsAnded, maintenanceWindow.relevantHostTagsAnded) &&
        Objects.equals(this.hostTagGroupHostNamesGroupAnded, maintenanceWindow.hostTagGroupHostNamesGroupAnded) &&
        Objects.equals(this.eventName, maintenanceWindow.eventName) &&
        Objects.equals(this.runningState, maintenanceWindow.runningState) &&
        Objects.equals(this.sortAttr, maintenanceWindow.sortAttr);
  }

  @Override
  public int hashCode() {
    return Objects.hash(reason, customerId, relevantCustomerTags, title, startTimeInSeconds, endTimeInSeconds, relevantHostTags, relevantHostNames, creatorId, updaterId, id, createdEpochMillis, updatedEpochMillis, relevantHostTagsAnded, hostTagGroupHostNamesGroupAnded, eventName, runningState, sortAttr);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class MaintenanceWindow {\n");

    sb.append("    reason: ").append(toIndentedString(reason)).append("\n");
    sb.append("    customerId: ").append(toIndentedString(customerId)).append("\n");
    sb.append("    relevantCustomerTags: ").append(toIndentedString(relevantCustomerTags)).append("\n");
    sb.append("    title: ").append(toIndentedString(title)).append("\n");
    sb.append("    startTimeInSeconds: ").append(toIndentedString(startTimeInSeconds)).append("\n");
    sb.append("    endTimeInSeconds: ").append(toIndentedString(endTimeInSeconds)).append("\n");
    sb.append("    relevantHostTags: ").append(toIndentedString(relevantHostTags)).append("\n");
    sb.append("    relevantHostNames: ").append(toIndentedString(relevantHostNames)).append("\n");
    sb.append("    creatorId: ").append(toIndentedString(creatorId)).append("\n");
    sb.append("    updaterId: ").append(toIndentedString(updaterId)).append("\n");
    sb.append("    id: ").append(toIndentedString(id)).append("\n");
    sb.append("    createdEpochMillis: ").append(toIndentedString(createdEpochMillis)).append("\n");
    sb.append("    updatedEpochMillis: ").append(toIndentedString(updatedEpochMillis)).append("\n");
    sb.append("    relevantHostTagsAnded: ").append(toIndentedString(relevantHostTagsAnded)).append("\n");
    sb.append("    hostTagGroupHostNamesGroupAnded: ").append(toIndentedString(hostTagGroupHostNamesGroupAnded)).append("\n");
    sb.append("    eventName: ").append(toIndentedString(eventName)).append("\n");
    sb.append("    runningState: ").append(toIndentedString(runningState)).append("\n");
    sb.append("    sortAttr: ").append(toIndentedString(sortAttr)).append("\n");
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

