from pyrogram.types import ReplyKeyboardMarkup
import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.time_button],
        [buttons.weather, buttons.weather_forecast],
    ],
    resize_keyboard=True,
)