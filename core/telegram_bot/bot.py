from aiogram import Dispatcher, Bot
from telegram_bot.handlers.authenticationgateway import authentication_router
from django.conf import settings



bot = Bot(settings.TOKEN_TELEGRAM_BOT, parse_mode='HTML')

async def main() -> None:
    
    dp = Dispatcher()
    
    dp.include_router(authentication_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)