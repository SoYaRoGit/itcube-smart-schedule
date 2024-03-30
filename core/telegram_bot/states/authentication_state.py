from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication,
    inline_keyboard_authentication_user_menu
)


authentication_state_router = Router()


@authentication_state_router.callback_query(F.data.in_('authentication_user'))
async def authentication_user_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['authentication_user_menu'],
        reply_markup = inline_keyboard_authentication_user_menu
    )
    
    await callback.answer()


@authentication_state_router.callback_query(F.data.in_('authentication_user_cancel'))
async def authentication_user_cancel(callback: CallbackQuery):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['cmd_start_not_authentication'],
        reply_markup = inline_keyboard_authentication
    )