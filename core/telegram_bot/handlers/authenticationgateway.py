from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from telegram_bot.filters.filter import NotAuthenticationFilter
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication,
    inline_keyboard_authentication_menu
)
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
        # Вызывает кнопку с авторизацией callback_data = authentication
        reply_markup = inline_keyboard_authentication 
    )


@authentication_router.callback_query(F.data.in_('authentication'))
async def authentication_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['authentication_menu'],
        reply_markup = inline_keyboard_authentication_menu
    )
    
    await callback.answer()


@authentication_router.callback_query(F.data.in_('authentication_backward'))
async def authentication_backward(callback: CallbackQuery):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['cmd_start_not_authentication'].format(callback.from_user.full_name),
        reply_markup = inline_keyboard_authentication
    )