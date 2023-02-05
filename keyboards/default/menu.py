from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оставить заявку'),
            KeyboardButton(text='Купить товар')
        ],
        [
            KeyboardButton(text='Баланс'),
        ]
    ],
    resize_keyboard=True
)
