import asyncpg

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import KeyboardButton
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.default.menu import menu
from loader import dp, db, bot
from states import spam

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if config.admin == str(message.from_user.id):
        menu.insert(
            KeyboardButton(
                text='Отправить сообщение пользователям')
        )
    await message.answer(f'Привет, {message.from_user.full_name}!',
                         reply_markup=menu

                         )

    try:
        await db.add_user(message.chat.id, message.chat.username)
    except asyncpg.exceptions.UniqueViolationError:
        pass

@dp.message_handler(text="Отправить сообщение пользователям")
async def spam(message: types.Message, state: FSMContext):
    await state.set_state('Spam')
    await message.answer('Напишите что-нибудь и все пользователи увидят это')
    await message.delete()

@dp.message_handler(content_types=['text'],state='Spam')
async def spam(message: types.Message, state: FSMContext):
    if config.admin == str(message.from_user.id):
        rec = await db.select_all_users()
        count = 0
        for user in [dict(st) for st in rec]:
            if str(user['id']) != config.admin:
                try:
                    await bot.send_message(chat_id=user['id'], text=message.text)
                    count+=1
                except:
                    await db.delete_user(user['id'])
        await message.answer(f'Сообщение отправлено {count} пользователям!')
        await state.reset_state()