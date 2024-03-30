from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from telegram_bot.filters.filter import NotAuthenticationFilter
from telegram_bot.keyboards.authentication_keyboard import inline_keyboard_authentication
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.states.authentication_state import authentication_state_router



authentication_router = Router()
authentication_router.include_router(authentication_state_router)


@authentication_router.message(CommandStart(), NotAuthenticationFilter())
async def cmd_start(message: Message):
    # Удалить сообщение /start
    await message.delete()
    
    # Отправка стартового сообщения для не авторизированных пользователей
    await message.answer(
        text = AUTHENTICATION_TEXT['cmd_start_not_authentication'].format(message.from_user.full_name),
        # Вызывает кнопку с авторизацией callback_data = authentication_user
        reply_markup = inline_keyboard_authentication 
    )