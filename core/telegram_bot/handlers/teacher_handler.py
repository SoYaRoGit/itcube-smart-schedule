from aiogram import Bot, Router, F, html
from aiogram.types import Message, CallbackQuery
from telegram_bot.filters.filter import AuthenticationTeacherFilter
from telegram_bot.keyboards.teacher_keyboard import inline_keyboard_panel, inline_keyboard_backward, builder_inline_keyboard_group
from telegram_bot.eduutils.edu_utils_db import get_teacher_send_personal_data, get_teacher_send_schedule, teacher_send_schedule_reminder
from telegram_bot.loader import scheduler, bot
from telegram_bot.states.teacher_message_state import teacher_message_state_router
from asgiref.sync import sync_to_async


teacher_handler = Router()
teacher_handler.include_router(teacher_message_state_router)
teacher_handler.message(AuthenticationTeacherFilter())


@teacher_handler.message(F.text == '/panel', AuthenticationTeacherFilter())
async def cmd_panel_teacher(message: Message):
    await message.delete()
    await message.answer(
        text = 'Панель преподавателя',
        reply_markup = inline_keyboard_panel,
        protect_content = True
    )


@teacher_handler.callback_query(F.data.in_('teacher_send_personal_data'))
async def teacher_send_personal_data(callback: CallbackQuery):
    personal_data = await sync_to_async(get_teacher_send_personal_data)(callback.from_user.id)
    
    entities = callback.message.entities or []  # Получение сущностей сообщения (если есть)
    for item in entities:
        if item.type in personal_data.keys():
            personal_data[item.type] = item.extract_from(callback.message.text)  # Извлечение информации из сущностей сообщения
        
    await callback.message.edit_text(
        f'📹 Данные учетной записи\n'
        f'Уникальный ID: {html.quote(str(personal_data["id"]))}\n'
        f'Логин: {html.quote(str(personal_data["login"]))}\n'
        f'Пароль: {html.quote(str(personal_data["password"]))}\n'
        f'ФИО: {html.quote(str(personal_data["full_name"]))}\n'
        f'Телеграм ID: {html.quote(str(personal_data["telegram_id"]))}\n'
        f'Статус аутентификации: {html.quote(str(personal_data["is_authentication"]))}\n',
        reply_markup = inline_keyboard_backward
        )
    
    await callback.answer()


@teacher_handler.callback_query(F.data.in_('teacher_send_schedule'))
async def teacher_send_schedule(callback: CallbackQuery):
    scheduele = await sync_to_async(get_teacher_send_schedule)(callback.from_user.id)
    if scheduele:
        await callback.message.answer(
            text="\n".join(str(item) for item in scheduele)
        )
    else:
        await callback.message.answer(
            text='В данный момент нет запланированных занятий'
        )
    
    await callback.answer()
    

async def notifying_teachers(bot: Bot):
    reminder = await sync_to_async(teacher_send_schedule_reminder)()
    
    for telegram_id, schedulers in reminder.items():
        if schedulers:
            for scheduler in schedulers:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=scheduler
                )
scheduler.add_job(notifying_teachers, "interval", seconds=60, kwargs={'bot': bot})


@teacher_handler.callback_query(F.data.in_('teacher_send_message_for_group'))
async def teacher_send_message_for_group(callback: CallbackQuery):
    keyboard = await builder_inline_keyboard_group(callback.from_user.id)
    await callback.message.edit_text(
        text = 'Выберите группу для отправки сообщения',
        reply_markup = keyboard
    )
    await callback.answer()


@teacher_handler.callback_query(F.data.in_('teacher_inline_keyboard_backward'))
async def teacher_inline_keyboard_backward(callback: CallbackQuery):
    await callback.message.edit_text(
        text = 'Панель преподавателя',
        reply_markup = inline_keyboard_panel
    )
    await callback.answer()


@teacher_handler.callback_query(F.data.in_('teacher_panel_cancel'))
async def teacher_panel_cancel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()