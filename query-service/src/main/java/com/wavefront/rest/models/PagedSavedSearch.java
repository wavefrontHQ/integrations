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

import com.wavefront.rest.models.SavedSearch;
import com.wavefront.rest.models.Sorting;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * PagedSavedSearch
 */
@javax.annotation.Generated(value = "io.swagger.codegen.languages.JavaClientCodegen", date = "2019-02-25T16:34:08.557+05:30")
public class PagedSavedSearch {
  @SerializedName("items")
  private List<SavedSearch> items = null;

  @SerializedName("offset")
  private Integer offset = null;

  @SerializedName("limit")
  private Integer limit = null;

  @SerializedName("cursor")
  private String cursor = null;

  @SerializedName("totalItems")
  private Integer totalItems = null;

  @SerializedName("moreItems")
  private Boolean moreItems = null;

  @SerializedName("sort")
  private Sorting sort = null;

  public PagedSavedSearch items(List<SavedSearch> items) {
    this.items = items;
    return this;
  }

  public PagedSavedSearch addItemsItem(SavedSearch itemsItem) {
    if (this.items == null) {
      this.items = new ArrayList<SavedSearch>();
    }
    this.items.add(itemsItem);
    return this;
  }

  /**
   * List of requested items
   *
   * @return items
   **/
  @ApiModelProperty(value = "List of requested items")
  public List<SavedSearch> getItems() {
    return items;
  }

  public void setItems(List<SavedSearch> items) {
    this.items = items;
  }

  /**
   * Get offset
   *
   * @return offset
   **/
  @ApiModelProperty(value = "")
  public Integer getOffset() {
    return offset;
  }

  public PagedSavedSearch limit(Integer limit) {
    this.limit = limit;
    return this;
  }

  /**
   * Get limit
   *
   * @return limit
   **/
  @ApiModelProperty(value = "")
  public Integer getLimit() {
    return limit;
  }

  public void setLimit(Integer limit) {
    this.limit = limit;
  }

  public PagedSavedSearch cursor(String cursor) {
    this.cursor = cursor;
    return this;
  }

  /**
   * The id at which the current (limited) search can be continued to obtain more matching items
   *
   * @return cursor
   **/
  @ApiModelProperty(value = "The id at which the current (limited) search can be continued to obtain more matching items")
  public String getCursor() {
    return cursor;
  }

  public void setCursor(String cursor) {
    this.cursor = cursor;
  }

  public PagedSavedSearch totalItems(Integer totalItems) {
    this.totalItems = totalItems;
    return this;
  }

  /**
   * An estimate (lower-bound) of the total number of items available for return.  May not be a tight estimate for facet queries
   *
   * @return totalItems
   **/
  @ApiModelProperty(value = "An estimate (lower-bound) of the total number of items available for return.  May not be a tight estimate for facet queries")
  public Integer getTotalItems() {
    return totalItems;
  }

  public void setTotalItems(Integer totalItems) {
    this.totalItems = totalItems;
  }

  public PagedSavedSearch moreItems(Boolean moreItems) {
    this.moreItems = moreItems;
    return this;
  }

  /**
   * Whether more items are available for return by increment offset or cursor
   *
   * @return moreItems
   **/
  @ApiModelProperty(value = "Whether more items are available for return by increment offset or cursor")
  public Boolean isMoreItems() {
    return moreItems;
  }

  public void setMoreItems(Boolean moreItems) {
    this.moreItems = moreItems;
  }

  public PagedSavedSearch sort(Sorting sort) {
    this.sort = sort;
    return this;
  }

  /**
   * Get sort
   *
   * @return sort
   **/
  @ApiModelProperty(value = "")
  public Sorting getSort() {
    return sort;
  }

  public void setSort(Sorting sort) {
    this.sort = sort;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    PagedSavedSearch pagedSavedSearch = (PagedSavedSearch) o;
    return Objects.equals(this.items, pagedSavedSearch.items) &&
        Objects.equals(this.offset, pagedSavedSearch.offset) &&
        Objects.equals(this.limit, pagedSavedSearch.limit) &&
        Objects.equals(this.cursor, pagedSavedSearch.cursor) &&
        Objects.equals(this.totalItems, pagedSavedSearch.totalItems) &&
        Objects.equals(this.moreItems, pagedSavedSearch.moreItems) &&
        Objects.equals(this.sort, pagedSavedSearch.sort);
  }

  @Override
  public int hashCode() {
    return Objects.hash(items, offset, limit, cursor, totalItems, moreItems, sort);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class PagedSavedSearch {\n");

    sb.append("    items: ").append(toIndentedString(items)).append("\n");
    sb.append("    offset: ").append(toIndentedString(offset)).append("\n");
    sb.append("    limit: ").append(toIndentedString(limit)).append("\n");
    sb.append("    cursor: ").append(toIndentedString(cursor)).append("\n");
    sb.append("    totalItems: ").append(toIndentedString(totalItems)).append("\n");
    sb.append("    moreItems: ").append(toIndentedString(moreItems)).append("\n");
    sb.append("    sort: ").append(toIndentedString(sort)).append("\n");
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

