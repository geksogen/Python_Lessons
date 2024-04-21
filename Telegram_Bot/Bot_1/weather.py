import datetime
import pyowm.commons.exceptions
import pytz
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyrogram import emoji

import config

def get_omw_client() -> OWM:
    owm_config = get_default_config()
    owm_config["language"] = "ru"

    return OWM(
        api_key = config.OWM_KEY,
        config = owm_config
    )

client = get_omw_client()

weather_emojis = {
'Thunderstorm': emoji.CLOUD_WITH_LIGHTNING_AND_RAIN,    # Гроза
'Drizzle': emoji.UMBRELLA_WITH_RAIN_DROPS,              # Морось
'Rain': emoji.CLOUD_WITH_RAIN,                          # Дождь
'Snow': emoji.SNOWFLAKE,                                # Снег
'Clear': emoji.SUN,                                     # Ясно
'Clouds': emoji.CLOUD,                                  # Облачно
}

def get_current_weather(city: str) -> str:
    mgr = client.weather_manager()

    try:
        obs = mgr.weather_at_place(city)
    except pyowm.commons.exceptions.NotFoundError:
        return  "Не найден город!"

    w = obs.weather
    status = w.detailed_status
    weather_emoji = weather_emojis.get(w.status, None)
    temp = w.temperature('celsius')['temp']
    temp_sign = '+' if temp > 0 else ''
    wind_speed = w.wind()['speed']
    humidity = w.humidity

    message = f'Погода в городе {city}:\n\n'
    message += f'{status.capitalize()} {weather_emoji}\n'
    message += f'Температура: {temp_sign}{temp:.1f} {emoji.THERMOMETER}\n'
    message += f'Ветер: {wind_speed:.1f} m/c {emoji.LEAF_FLUTTERING_IN_WIND}\n'
    message += f'Влажность: {humidity}% {emoji.DROPLET}'

    return message

def get_forecast(city: str) -> str:
    mgr = client.weather_manager()

    try:
        forecaster = mgr.forecast_at_place(city, '3h')
    except pyowm.commons.exceptions.NotFoundError:
        return  "Не найден город!"

    weather_list = forecaster.forecast.weathers

    dates = []
    today = datetime.datetime.now(pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    for day in range(1, 4):
        for hour in range(0, 24, 6):
            dates.append(today + datetime.timedelta(days=day, hours=hour))

    weather_list = list(filter(lambda x: x.reference_time('date') in dates, weather_list))

    hours = {
        0: f'{emoji.CRESCENT_MOON} Ночь',
        6: f'{emoji.SUNRISE} Утро',
        12: f'{emoji.SUN} День',
        18: f'{emoji.SUNSET} Вечер'
    }

    day_names = ['Завтра', 'Послезавтра', 'Через 3 дня']
    forecast = f'{emoji.CALENDAR} Прогноз погоды {city} на 3 дня:\n\n'

    for day in range(3):
        forecast += f"{day_names[day]}:\n"
        for hour in range(4):
            weather = weather_list[day * 4 + hour]
            status = weather.detailed_status
            temp = weather.temperature('celsius')['temp']
            temp_sign = '+' if temp > 0 else ''
            emoji_icon = weather_emojis.get(weather.status, None)
            hour = weather.reference_time('date').hour

            forecast += f"{hours[hour]}: {temp_sign}{temp:.0f}°C, {status} {emoji_icon}\n"
        forecast += "\n"

    return forecast

print(get_forecast('Kaluga'))


