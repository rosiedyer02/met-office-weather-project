from parser import parse_forecast

def test_parse_forecast_extracts_expected_fields():
    sample_response = {
        "features": [
            {
                "properties": {
                    "timeSeries": [
                        {
                            "time": "2026-07-23T00:00Z",
                            "nightMinScreenTemperature": 14.19,
                        },
                        {
                            "time": "2026-07-24T00:00Z",
                            "dayMaxScreenTemperature": 24.97,
                            "nightMinScreenTemperature": 14.37,
                            "dayProbabilityOfPrecipitation": 1,
                            "midday10MWindSpeed": 4.49,
                        },
                    ]
                }
            }
        ]
    }

    result = parse_forecast(sample_response)

    assert len(result) == 2

    # First day: partial, should be flagged and missing fields should be None
    assert result[0]["is_partial_day"] is True
    assert result[0]["max_temp_c"] is None
    assert result[0]["min_temp_c"] == 14.19

    # Second day: full day, all fields present
    assert result[1]["is_partial_day"] is False
    assert result[1]["max_temp_c"] == 24.97
    assert result[1]["chance_of_rain_percent"] == 1