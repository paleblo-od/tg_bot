from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

profile_keyboard = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[

                                               [InlineKeyboardButton(
                                                    text='Закрыть',
                                                   callback_data='close')]

                                        ]
                                        )