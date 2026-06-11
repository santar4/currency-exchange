import aiohttp
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def normalize_currency(value: str) -> str:
    return value.strip().upper()


async def get_response(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

def cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Cancel")
    markup = builder.as_markup()
    markup.resize_keyboard = True
    print('Cancel')
    return markup


