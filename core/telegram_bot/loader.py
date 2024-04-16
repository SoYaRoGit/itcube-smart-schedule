from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
