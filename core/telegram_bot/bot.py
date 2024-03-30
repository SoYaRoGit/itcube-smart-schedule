from telegram_bot import loader
from telegram_bot.utils.logger import logger
from telegram_bot.handlers.authenticationgateway import authentication_router



async def main() -> None:
    
    logger.info('Запуск бота')
    
    bot = loader.bot
    dp = loader.dp
    
    dp.include_router(authentication_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)