from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    GetBudget = State()
    GetNumber = State()
