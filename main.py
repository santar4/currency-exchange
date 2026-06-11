import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import fsm
import handler
from settings import form_router, token


async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(handler.router)
    dp.include_router(form_router)
    await bot.set_my_commands(commands=[
        types.BotCommand(command="/start", description='Start bot'),
        types.BotCommand(command="/currencies", description='View all currencies'),
        types.BotCommand(command="/convert", description='Convert currency'),
    ]
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






