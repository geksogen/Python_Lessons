from pyrogram.types import KeyboardButton
from pyrogram import emoji


time_button = KeyboardButton(f'{emoji.ALARM_CLOCK} Время')
weather = KeyboardButton(f'{emoji.CLOUD} Погода')
weather_forecast = KeyboardButton(f'{emoji.SUN} Прогноз на 3 дня')
