import time
import random
from weather import get_current_weather
import pyrogram
import config
from pyrogram.types import Message
from pyrogram import Client, filters
import buttons
import keyboards
from custom_filters import button_filter
from config import BOT_TOKEN, API_ID, API_HASH


bot = Client(
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    bot_token= config.BOT_TOKEN,
    name= "Echo_bot"
)

#@bot.on_message()
#async def echo(client: Client, message: Message):
#    await message.reply(message.text)

@bot.on_message(filters=filters.command('start') | button_filter(buttons.back_button))
async def time_command(client: Client, message: Message):
    await message.reply(f"Привет я бот, который умеет показывать время. Нажми на кнопку {buttons.help_button.text} для получения списка команд.", reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command('time') | button_filter((buttons.time_button)))    #время
async def time_command(client: Client, message: Message):
    current_time = time.strftime('%H:%M:%S')
    await message.reply(f'Текущее время: {current_time}')

@bot.on_message(filters=filters.command('weather') | button_filter((buttons.weather)))
async def weather_command(client: Client, message: Message):
    if message.command and len(message.command) > 1:
        city = message.command[1]
    else:
        city = 'Moscow'

    weather = get_current_weather(city)
    await message.reply(weather)


bot.run()