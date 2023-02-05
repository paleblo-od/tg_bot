from loader import db
from utils.db_api import create_table


async def on_startup(dp):
    # import filters
    #import middlewares
    # filters.setup(dp)
    #middlewares.setup(dp)
    await create_table.run()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
