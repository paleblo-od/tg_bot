from aiogram import types

from keyboards.inline.balance import profile_keyboard
from loader import dp, db
from utils.db_api.yookass import get_payments_from_user

@dp.message_handler(commands=['/balance'])
@dp.message_handler(text='Баланс')
async def bot_start(message: types.Message):
    await message.delete()
    user = message.from_user
    result = await db.select_user(id=user.id)

    total_history_balance = 0
    payments = await get_payments_from_user(user_id=user.id)
    for payment in payments:
        total_history_balance += float(payment.get('sum'))
    await message.answer(f'<b>ИД:</b>  {user.id}\n'
                         f'<b>Никнейм:</b> @{user.username}\n'
                         f'<b>Текущий баланс:</b> {result.get("balance")}\n'
                         f'<b>Сумма всех пополнений:</b> {total_history_balance}\n',
                         reply_markup=profile_keyboard
                         )


@dp.callback_query_handler(text='close')
async def cancel(cl: types.CallbackQuery):
    await cl.message.delete()
