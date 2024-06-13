from telegram_bot import loader
from telegram_bot.handlers.authenticationgateway import authentication_router
from telegram_bot.handlers.student_handler import student_handler
from telegram_bot.handlers.teacher_handler import teacher_handler
from telegram_bot.keyboards.set_menu import set_main_menu
from telegram_bot.utils.logger import logger

async def main() -> None:
    """
    Основная функция для запуска телеграм-бота.
    """

    # Логирование информации о запуске бота
    logger.info("Запуск бота")

    # Получение объектов бота, диспетчера и планировщика из загрузчика
    bot = loader.bot
    dp = loader.dp
    scheduler = loader.scheduler

    # Подключение обработчиков сообщений для студентов, преподавателей и аутентификации
    dp.include_router(student_handler)
    dp.include_router(teacher_handler)
    dp.include_router(authentication_router)

    # Запуск планировщика задач
    scheduler.start()

    # Установка меню
    await set_main_menu(bot)

    # Удаление вебхука, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск опроса для получения входящих сообщений
    await dp.start_polling(bot)
