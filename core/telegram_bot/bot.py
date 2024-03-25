from aiogram import Dispatcher, Bot
from django.conf import settings


async def main() -> None:
    bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode='HTML')
    dp = Dispatcher()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)