from telegram_bot import loader
from telegram_bot.utils.logger import logger
from telegram_bot.handlers.authenticationgateway import authentication_router
from telegram_bot.handlers.student_handler import student_handler
from telegram_bot.handlers.teacher_handler import teacher_handler
from telegram_bot.keyboards.set_menu import set_main_menu


async def main() -> None:
    
    logger.info('Запуск бота')
    
    bot = loader.bot
    dp = loader.dp
    scheduler = loader.scheduler
    
    
    dp.include_router(student_handler)
    dp.include_router(teacher_handler)
    dp.include_router(authentication_router)
    scheduler.start()
    
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)