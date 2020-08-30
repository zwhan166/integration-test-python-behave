import json

import requests
from behave import when, then
from hamcrest import assert_that


@when('we get zippopotam data from "{url}"')
def step_impl(context, url):
    response = requests.get(url)
    context.zippopotam = {
        "response": response,
        "data": json.loads(response.text)
    }


@then('zippopotam\'s response status code is {status_code:d}')
def step_impl(context, status_code):
    assert_that(status_code == context.zippopotam["response"].status_code)


@then('zippopotam\'s response content type is "{content_type}"')
def step_impl(context, content_type):
    assert_that(content_type == context.zippopotam["response"].headers["content-type"])


@then('zippopotam\'s response time is less than {duration:d}s')
def step_impl(context, duration):
    assert_that(context.zippopotam["response"].elapsed.total_seconds() <= duration)


@then('zippopotam\'s response data has fields as below')
def step_impl(context):
    for row in context.table:
        val = context.zippopotam["data"][row["field"]]
        assert_that(val == row["value"])


@then('zippopotam\'s response data has place items as below')
def step_impl(context):
    for row in context.table:
        place = None
        for item in context.zippopotam["data"]["places"]:
            if item["post code"] == row["post code"]:
                place = item
                break
        assert_that(place, "Failed to find the place with post code {}!".format(row["post code"]))
        assert_that(place["place name"] == row["place name"])


@when('we run the data-driven test on zippopotam\'s data')
def step_impl(context):
    for row in context.table:
        context.execute_steps("""
            When we get zippopotam data from "http://api.zippopotam.us/{}/{}"
            Then zippopotam's response status code is 200
             And zippopotam's response content type is "application/json"
    	     And zippopotam's response time is less than 1s
    	     And zippopotam's response data has place "{}" for postal code "{}"
        """.format(row["country"], row["postal code"], row["place name"], row["postal code"]))


@then('zippopotam\'s response data has place "{place_name}" for postal code "{post_code}"')
def step_impl(context, place_name, post_code):
    assert_that(context.zippopotam["data"]["post code"] == post_code)
    assert_that(len(context.zippopotam["data"]["places"]) == 1)
    assert_that(context.zippopotam["data"]["places"][0]["place name"] == place_name)

