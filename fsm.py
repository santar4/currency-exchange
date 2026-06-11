from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from exchange.api import all_currencies, convert_currency
from exchange.tools import normalize_currency, cancel_keyboard
from form import ConvertForm
from settings import form_router

@form_router.message(F.text == "Cancel")
async def cmd_cancel(message: Message):
    await message.answer("Convertation has been canceled", reply_markup=ReplyKeyboardRemove())

@form_router.message(Command('convert'))
async def convert_start(message: Message, state: FSMContext) -> None:
    await state.set_state(ConvertForm.based_currency)
    await message.answer(
        "Type currency that you prefer to exchange (USD for example)",
        reply_markup=cancel_keyboard()
    )



@form_router.message(ConvertForm.based_currency)
async def based_currency_name(message: Message, state: FSMContext) -> None:
    based_currency = normalize_currency(message.text)
    currencies = []
    exchange_currencies = []
    await all_currencies(exchange_currencies, currencies)

    if based_currency not in exchange_currencies:
        await message.answer('Your currency isn`t available, try /currencies')
        return

    await state.update_data(based_currency=based_currency)
    await state.set_state(ConvertForm.amount)
    await message.answer("Type amount:")



@form_router.message(ConvertForm.amount)
async def currency_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = float(message.text)
    except (AttributeError, ValueError):
        await message.answer('It is not a number')
        return

    if amount <= 0:
        await message.answer('Your value must be bigger than 0')
        return

    await state.update_data(amount=amount)
    await state.set_state(ConvertForm.quoted_currency)
    await message.answer('Type preferred currency to change (EUR for example)')



@form_router.message(ConvertForm.quoted_currency)
async def quoted_currency_name(message: Message, state: FSMContext) -> None:
    quoted_currency = normalize_currency(message.text)
    currencies = []
    exchange_currencies = []
    await all_currencies(exchange_currencies, currencies)
    if quoted_currency not in exchange_currencies:
        await message.answer('Your currency isn`t available')
        return
    await state.update_data(quoted_currency=message.text)

    data = await state.get_data()
    amount = data['amount']
    based_currency = data['based_currency']
    result = await convert_currency(
        amount, based_currency, quoted_currency
    )
    await state.clear()
    await message.answer(f"{amount:g} {based_currency} = {result:.2f} {quoted_currency}")

