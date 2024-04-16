from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings


scheduler = AsyncIOScheduler(timezone = "Europe/Moscow")
bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())