from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings


bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())