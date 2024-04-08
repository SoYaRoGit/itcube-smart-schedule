from telegram_bot import loader
from telegram_bot.utils.logger import logger
from telegram_bot.handlers.authenticationgateway import authentication_router
from telegram_bot.handlers.student_handler import student_handler


async def main() -> None:
    
    logger.info('Запуск бота')
    
    bot = loader.bot
    dp = loader.dp
    scheduler = loader.scheduler
    
    
    dp.include_router()
    dp.include_router(student_handler)
    dp.include_router(authentication_router)
    scheduler.start()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)