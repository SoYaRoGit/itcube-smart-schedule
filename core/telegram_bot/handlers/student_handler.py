from aiogram import Router, F, html, Bot
from aiogram.types import Message, CallbackQuery
from telegram_bot.filters.filter import AuthenticationStudentFilter
from telegram_bot.eduutils.edu_utils_db import (
    get_student_send_personal_data, 
    get_student_send_schedule,
    send_schedule_reminder
)
from telegram_bot.keyboards.student_keyboard import inline_keyboard_panel, inline_keyboard_backward
from asgiref.sync import sync_to_async
from telegram_bot.loader import scheduler, bot

# Инициализация роутера
student_handler = Router()

# Пременить фильтр для всех сообщений, для учеников который аутентифицированы
student_handler.message.filter(AuthenticationStudentFilter())
student_handler.callback_query.filter(AuthenticationStudentFilter())


@student_handler.message(F.text == '/panel')
async def cmd_panel_student(message: Message):
    await message.delete()
    await message.answer(
        text = 'Панель обучающегося',
        reply_markup = inline_keyboard_panel
    )
    

@student_handler.callback_query(F.data.in_('student_send_personal_data'))
async def student_send_personal_data(callback: CallbackQuery):
    personal_data = await sync_to_async(get_student_send_personal_data)(callback.from_user.id)
    
    entities = callback.message.entities or []  # Получение сущностей сообщения (если есть)
    for item in entities:
        if item.type in personal_data.keys():
            personal_data[item.type] = item.extract_from(callback.message.text)  # Извлечение информации из сущностей сообщения
        
    await callback.message.edit_text(
        f'📹 Ваши персональные данные\n'
        f'Уникальный ID: {html.quote(str(personal_data["id"]))}\n'
        f'Логин: {html.quote(str(personal_data["login"]))}\n'
        f'Пароль: {html.quote(str(personal_data["password"]))}\n'
        f'ФИО: {html.quote(str(personal_data["full_name"]))}\n'
        f'Телеграм ID: {html.quote(str(personal_data["telegram_id"]))}\n'
        f'Статус аутентификации: {html.quote(str(personal_data["is_authentication"]))}\n',
        reply_markup = inline_keyboard_backward
        )
    
    await callback.answer()


@student_handler.callback_query(F.data.in_('student_send_schedule'))
async def student_send_schedule(callback: CallbackQuery):
    scheduele = await sync_to_async(get_student_send_schedule)(callback.from_user.id)
    await callback.message.answer(
        text="\n".join(str(item) for item in scheduele)
    )
    
    await callback.answer()
    

@student_handler.message()
async def test_scheduler(bot: Bot):
    reminder = await sync_to_async(send_schedule_reminder)()
    
    for telegram_id, schedulers in reminder.items():
        if schedulers:
            for scheduler in schedulers:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=scheduler
                )
    print(reminder)
scheduler.add_job(test_scheduler, "interval", seconds=60, kwargs={'bot': bot})


@student_handler.callback_query(F.data.in_('student_inline_keyboard_backward'))
async def student_inline_keyboard_backward(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Панель обучающегося',
        reply_markup= inline_keyboard_panel
    )
    await callback.answer()