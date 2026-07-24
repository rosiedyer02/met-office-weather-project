def parse_forecast(raw_response):
    # Extract the fields we care about from a from a Datahub daily forecast response
    features = raw_response["features"]
    time_series = features[0]["properties"]["timeSeries"]

    daily_forecasts = []
    for day in time_series:
        daily_forecasts.append({
            "time": day.get("time"),
            "max_temp_c": day.get("dayMaxScreenTemperature"),
            "min_temp_c": day.get("nightMinScreenTemperature"),
            "chance_of_rain_percent": day.get("dayProbabilityOfPrecipitation"),
            "max_wind_speed": day.get("midday10MWindSpeed"),
            # If the model run happens after the day's daylight hours have already happened,
            # only the night fields are present, flag this partial day here.
            "is_partial_day": day.get("dayMaxScreenTemperature") is None,
        })
    return daily_forecasts