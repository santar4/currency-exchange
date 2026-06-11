import os
from dotenv import load_dotenv
from aiogram import Router


load_dotenv()
token = os.getenv("BOT_TOKEN")
form_router = Router()
