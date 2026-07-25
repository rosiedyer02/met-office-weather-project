import boto3
from decimal import Decimal

TABLE_NAME = "weather-forecasts"

def _convert_floats_to_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {key: _convert_floats_to_decimal(value) for key, value in obj.items()}
    return obj

def save_forecasts(location, forecasts, dynamodb_resource=None):
    dynamodb = dynamodb_resource or boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    for day in forecasts:
        item = _convert_floats_to_decimal({
            "location": location,
            **day
        })
        table.put_item(Item=item)