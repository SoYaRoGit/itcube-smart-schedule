from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication_cancel
)



authentication_state_router = Router()


class FSMAuthenticationForm(StatesGroup):
    LOGIN = State()
    PASSWORD = State()


@authentication_state_router.callback_query(F.data.in_('authentication_user_state_login'))
async def authentication_user_continue(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['authentication_user_state_login'],
        reply_markup = inline_keyboard_authentication_cancel
    )
    
    # Запоминаем ID чата и ID сообщения для его последующего обновления
    await state.update_data(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id
    )
    
    await state.set_state(
        state = FSMAuthenticationForm.LOGIN
    )
    
    await callback.answer()