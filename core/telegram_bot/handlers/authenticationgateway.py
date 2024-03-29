from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from telegram_bot.keyboards.authentication_keyboard import inline_keyboard_authentication
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT

authrouter = Router()


# Обработчик заглушка для проверки работы бота
@authrouter.message(CommandStart)
async def cmd_start(message: Message):
    # Удалить сообщение /start
    await message.delete()
    
    # Отправка стартового сообщения для не авторизированных пользователей
    await message.answer(
        text = AUTHENTICATION_TEXT['cmd_start_not_authentication'].format(message.from_user.full_name),
        reply_markup = inline_keyboard_authentication 
    )