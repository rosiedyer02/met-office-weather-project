import json
import boto3
from decimal import Decimal

TABLE_NAME = "weather-forecasts"

def _decimal_to_native(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, dict):
        return {key: _decimal_to_native(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_decimal_to_native(item) for item in obj]
    return obj

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    query_params = event.get("queryStringParameters") or {}
    location = query_params.get("location", "Plymouth")

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("location").eq(location)
    )

    items = _decimal_to_native(response["Items"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }