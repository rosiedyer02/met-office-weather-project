import json
import boto3
from moto import mock_aws
from read_forecast import lambda_handler

TABLE_NAME = "weather-forecasts"

@mock_aws
def test_lamda_handler_returns_forecast_for_location():
    # Set up a real table, matching the real one's structure
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "location", "KeyType": "HASH"},
            {"AttributeName": "time", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "location", "AttributeType": "S"},
            {"AttributeName": "time", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table = dynamodb.Table(TABLE_NAME)

    # Put known data directly into the fake table
    table.put_item(Item={
        "location": "Plymouth",
        "time": "2026-07-24T00:00Z",
        "max_temp_c": 22,
        "min_temp_c": 14,
    })

    # Simulate an API Gateway event with a location query param
    event = {"queryStringParameters": {"location": "Plymouth"}}

    result = lambda_handler(event, context=None)

    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert len(body) == 1
    assert body[0]["location"] == "Plymouth"
    assert body[0]["max_temp_c"] == 22

@mock_aws
def test_lamda_handler_defaults_to_plymouth_with_no_query_params():
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "location", "KeyType": "HASH"},
            {"AttributeName": "time", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "location", "AttributeType": "S"},
            {"AttributeName": "time", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table = dynamodb.Table(TABLE_NAME)

    # Put known data directly into the fake table
    table.put_item(Item={
        "location": "Plymouth",
        "time": "2026-07-24T00:00Z",
        "max_temp_c": 22,
        "min_temp_c": 14,
    })

    # No queryStringParameters key at all, mimics hitting the URL directly
    event = {"queryStringParameters": None}

    result = lambda_handler(event, context=None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body[0]["location"] == "Plymouth"
