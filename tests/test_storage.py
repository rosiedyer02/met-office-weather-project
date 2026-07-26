import boto3
from moto import mock_aws
from storage import save_forecasts
from decimal import Decimal

TABLE_NAME = "weather-forecasts"

@mock_aws
def test_save_forecasts_writes_items_to_table():
    # Fake DynamoDB table, matching the structure of the real table
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "location", "KeyType": "HASH"},
            {"AttributeName": "time", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "location", "AttributeType": "S"},
            {"AttributeName": "time", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table = dynamodb.Table(TABLE_NAME)

    forecasts = [
        {"time": "2026-07-24T00:00Z", "max_temp_c": 24.97, "min_temp_c": 14.37},
        {"time": "2026-07-25T00:00Z", "max_temp_c": 23.95, "min_temp_c": 18.02},
    ]

    save_forecasts("Plymouth", forecasts, dynamodb_resource=dynamodb)

    response = table.scan()
    items = response["Items"]

    assert len(items) == 2
    assert items[0]["location"] == "Plymouth"
    assert any(item["max_temp_c"] == Decimal("24.97") for item in items)