from aiogram import Router, F
from aiogram.types import Message
from telegram_bot.filters.filter import NotAuthenticationFilter


# Инициализация роутера
student_handler = Router()

# Пременить фильтр для всех сообщений, для учеников который аутентифицированы
student_handler.message.filter(~NotAuthenticationFilter())