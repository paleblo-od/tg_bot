from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.yookassa_pay import Payed



async def product_inline():
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Купить 1 раз',
                                              callback_data='100'
                                          ),
                                      InlineKeyboardButton(
                                          text='Купить 2 раза',
                                          callback_data='200'
                                      )
                                  ]])
    markup.insert(
        InlineKeyboardButton(
            text='закрыть',
            callback_data='close')
        )
    return markup


async def pay_inline(payment: Payed):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Оплатить',
                                              url=payment.link,
                                              callback_data=""
                                          ),

                                  ]])
    return markup