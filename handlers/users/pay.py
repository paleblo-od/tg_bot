
from aiogram import types

from data import config
from keyboards.inline.pay import pay_inline, product_inline
from loader import dp

from utils.yookassa_pay import Payed

from utils.db_api.yookass import add_payment
from utils.db_api.user import add_balance

@dp.callback_query_handler(text='close')
async def cancel(cl: types.CallbackQuery):
    await cl.message.delete()

@dp.message_handler(text='Купить товар')
async def up_balance(message: types.Message):
    markup = await product_inline()
    await message.answer("Выбери", reply_markup= markup)

@dp.callback_query_handler()
async def cancel_payment(call: types.CallbackQuery):
    payment = Payed(call.data)
    await payment.create()
    markup = await pay_inline(payment)
    text = 'Для пополнения баланса, нажмите на кнопку оплаты'
    await call.message.edit_text(text=text,reply_markup=markup)
    await payment.start_check(call.message)
    await add_payment(str(payment.id), call.from_user.id, call.data, 'yookassa')
    await add_balance(user_id=call.from_user.id, value=call.data)
    await call.message.edit_text(f'Баланс успешно пополнен на {call.data}')