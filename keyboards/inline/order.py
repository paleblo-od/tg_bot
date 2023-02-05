from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData



menu_cd = CallbackData('show_menu', 'level', 'set')
buy_item = CallbackData('buy', 'item_id', 'count')


def make_callback_data(level,set="None"):
    return menu_cd.new(level=level,set=set)


async def Order_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = ["Продажа", "Производство", "Оказание услуг"]
    for button in buttons:
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, set=button)
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup


async def Platform_keyboard():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = ["Телеграм", "Ватсап", "Вайбер"]
    for button in buttons:
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,set=button)
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, set='df')
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup


def Budget_keyboard():
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,set="button")
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup


def Number_keyboard():
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup
