from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

# Создание асинхронного планировщика задач
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Создание объекта телеграм-бота
bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode="HTML")

# Создание диспетчера для обработки входящих сообщений бота
dp = Dispatcher(storage=MemoryStorage())
