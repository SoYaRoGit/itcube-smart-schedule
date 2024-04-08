from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegram_bot.filters.filter import AuthenticationTeacherFilter
from telegram_bot.keyboards.teacher_keyboard import inline_keyboard_panel



teacher_handler = Router()

teacher_handler.message(AuthenticationTeacherFilter())


@teacher_handler.message(F.text == '/panel')
async def cmd_panel_teacher(message: Message):
    await message.delete()
    await message.answer(
        text = 'Панель преподавателя',
        reply_markup = inline_keyboard_panel
    )
