import datetime
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.inline.order import Order_keyboard, Platform_keyboard, Budget_keyboard, menu_cd, Number_keyboard
from loader import dp

from loader import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sched = AsyncIOScheduler()
async def __alert(message: types.Message):
    await message.answer("Вы забыли заполнить заявку!")
    sched.shutdown()

@dp.message_handler(text='Оставить заявку')
async def bot_start(message: types.Message):
    try:
        sched.add_job(__alert, 'interval', [message], seconds=600, id="timer")
        sched.start()
    except Exception as e:
        pass
    await order_dialog(message)


@dp.message_handler(content_types='text',state='GetNumber',)
async def get_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id=int(config.admin), text=f"*Заявка* @{message.chat.username}:\n"
                                                           f"*Направление*: {data['1']}\n"
                                                           f"*Платформа*: {data['2']}\n" 
                                                           f"*Бюджет*: {data['budget']}\n"
                                                           f"*Номер*: `{message.text}`",parse_mode="Markdown")
    await data['call'].message.delete()
    await message.answer('Заявка отправлена!')
    await message.delete()
    await state.reset_state()
    sched.shutdown()

@dp.message_handler(content_types='text',state='GetBudget')
async def get_budget(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({'budget': message.text})
    data = await state.get_data()
    await number_dialog(data['call'],state)

@dp.callback_query_handler(text='cancel')
async def cancel(cl: types.CallbackQuery):
    sched.shutdown()
    await cl.answer('Отменено')
    await cl.message.delete()
    bot = dp.bot
    await bot.send_message(cl.from_user.id, 'Отменено')


async def order_dialog(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await Order_keyboard()
    if isinstance(message, types.Message):
        await message.answer('Какое направление вашего бизнеса?',
                             reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def platform_dialog(callback: types.CallbackQuery, **kwargs):
    markup = await Platform_keyboard()
    print(callback.data)
    await callback.message.edit_text('На какой платформе вы хотите разрабатывать чат-бота?',
                                     reply_markup=markup)

async def budget_dialog(callback: types.CallbackQuery,state: FSMContext, **kwargs):
    await state.set_state('GetBudget')
    markup = Budget_keyboard()
    await state.update_data({'call':callback})
    await callback.message.edit_text("Какой у вас бюджет? От... До...",
                                     reply_markup=markup)

async def number_dialog(callback: types.CallbackQuery, state: FSMContext, **kwargs):
    await state.set_state('GetNumber')
    markup = Number_keyboard()
    await callback.message.edit_text("Отправтьте свой номер",
                                     reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict,  state: FSMContext):
    print(callback_data)
    current_level = callback_data.get('level')
    await state.update_data({current_level:callback_data.get('set')})
    levels = {
        '0': order_dialog,
        '1': platform_dialog,
        '2': budget_dialog,
        '3': number_dialog
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        state = state
    )
