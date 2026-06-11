from aiogram.fsm.state import StatesGroup, State


class ConvertForm(StatesGroup):
    amount = State()
    based_currency = State()
    quoted_currency = State()
