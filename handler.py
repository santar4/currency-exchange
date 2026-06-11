from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from exchange.api import all_currencies
from settings import form_router

router = Router()

@form_router.message(Command('/start'))
async def start(message: Message):
    await message.answer('Hello')


@form_router.message(Command('currencies'))
async def show_currencies_handler(message: Message) -> None:
    currencies = []
    exchange_currencies = []
    await all_currencies(exchange_currencies, currencies)
    currencies_txt = ", \n".join(currencies)
    await message.answer(f"All supported currencies - {currencies_txt}")