from aiogram import Bot, F, Router, html
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from telegram_bot.eduutils.edu_utils_db import (
    get_student_confidential_data,
    get_student_send_personal_data,
    get_student_send_schedule,
    student_send_schedule_reminder,
)
from telegram_bot.filters.filter import AuthenticationStudentFilter
from telegram_bot.keyboards.student_keyboard import (
    inline_keyboard_backward,
    inline_keyboard_panel,
)
from telegram_bot.loader import bot, scheduler

# Создание роутера для обработки сообщений учеников
student_handler = Router()

# Применить фильтр для всех сообщений от аутентифицированных учеников
student_handler.message(AuthenticationStudentFilter())

# Применить фильтр для всех коллбэков от аутентифицированных учеников
student_handler.callback_query(AuthenticationStudentFilter())


@student_handler.message(F.text == "/panel")
async def cmd_panel_student(message: Message):
    """
    Обработчик команды "/panel" для обучающихся.

    Удаляет сообщение с командой и отправляет сообщение с панелью обучающегося.

    Args:
        message (Message): Входящее сообщение.

    Returns:
        None
    """
    await message.delete()
    await message.answer(
        text="Панель обучающегося",
        reply_markup=inline_keyboard_panel,
        protect_content=True,
    )


@student_handler.callback_query(F.data.in_("student_send_personal_data"))
async def student_send_personal_data(callback: CallbackQuery):
    """
    Обработчик запроса на отправку персональных данных обучающегося.

    Args:
        callback (CallbackQuery): Объект обратного вызова.

    Returns:
        None
    """
    personal_data = await sync_to_async(get_student_send_personal_data)(
        callback.from_user.id
    )

    entities = (
        callback.message.entities or []
    )  # Получение сущностей сообщения (если есть)
    for item in entities:
        if item.type in personal_data.keys():
            personal_data[item.type] = item.extract_from(
                callback.message.text
            )  # Извлечение информации из сущностей сообщения

    await callback.message.edit_text(
        f'📹 Данные учетной записи\n'
        f'Уникальный ID: {html.quote(str(personal_data["id"]))}\n'
        f'Логин: {html.quote(str(personal_data["login"]))}\n'
        f'Пароль: {html.quote(str(personal_data["password"]))}\n'
        f'ФИО: {html.quote(str(personal_data["full_name"]))}\n'
        f'Телеграм ID: {html.quote(str(personal_data["telegram_id"]))}\n'
        f'Статус аутентификации: {html.quote(str(personal_data["is_authentication"]))}\n',
        reply_markup=inline_keyboard_backward,
    )

    await callback.answer()


@student_handler.callback_query(F.data.in_("student_send_confidential_data"))
async def student_send_confidential_data(callback: CallbackQuery):
    """
    Обработчик запроса на отправку конфиденциальных данных обучающегося.

    Args:
        callback (CallbackQuery): Объект обратного вызова.

    Returns:
        None
    """
    confidential_data = await sync_to_async(get_student_confidential_data)(
        callback.from_user.id
    )

    entities = (
        callback.message.entities or []
    )  # Получение сущностей сообщения (если есть)
    for item in entities:
        if item.type in confidential_data.keys():
            confidential_data[item.type] = item.extract_from(
                callback.message.text
            )  # Извлечение информации из сущностей сообщения

    await callback.message.edit_text(
        f'📹 Конфиденциальные данные\n'
        f'ФИО Родителя: {html.quote(str(confidential_data["parent_full_name"]))}\n'
        f'Место регистрации родителя: {html.quote(str(confidential_data["parent_residential_adress"]))}\n'
        f'Дата рождения: {html.quote(str(confidential_data["date_birth"]))}\n'
        f'14-ий возраст: {html.quote(str(confidential_data["if_fourteen"]))}\n'
        f'Адрес проживания: {html.quote(str(confidential_data["student_residential_adress"]))}\n'
        f'Паспортные данные: {html.quote(str(confidential_data["passport_data"]))}\n'
        f'Кем выдан паспорт: {html.quote(str(confidential_data["passport_data_issued_by"]))}\n'
        f'Дата выдачи паспорта: {html.quote(str(confidential_data["passport_data_date_of_issueс"]))}\n'
        f'Учебная организация: {html.quote(str(confidential_data["name_education_organization"]))}\n'
        f'Номер сертификата: {html.quote(str(confidential_data["certificate_number"]))}\n'
        f'Контактные данные родителя: {html.quote(str(confidential_data["parent_contact"]))}\n'
        f'Контактные данные ученика: {html.quote(str(confidential_data["student_contact"]))}\n'
        f'Медицинские ограничения: {html.quote(str(confidential_data["medical_restrictions"]))}\n'
        f'Дата заключения контракта: {html.quote(str(confidential_data["date_contract"]))}\n',
        reply_markup=inline_keyboard_backward,
    )
    await callback.answer()


@student_handler.callback_query(F.data.in_("student_send_schedule"))
async def student_send_schedule(callback: CallbackQuery):
    """
    Обработчик запроса на отправку расписания занятий обучающегося.

    Args:
        callback (CallbackQuery): Объект обратного вызова.

    Returns:
        None
    """
    scheduele = await sync_to_async(get_student_send_schedule)(callback.from_user.id)
    if scheduele:
        await callback.message.answer(text="\n".join(str(item) for item in scheduele))
    else:
        await callback.message.answer(
            text="В данный момент нет запланированных занятий"
        )

    await callback.answer()


async def notifying_student(bot: Bot):
    """
    Асинхронная функция для уведомления обучающихся о предстоящих занятиях.

    Args:
        bot (Bot): Объект бота.

    Returns:
        None
    """
    reminder = await sync_to_async(student_send_schedule_reminder)()

    for telegram_id, schedulers in reminder.items():
        if schedulers:
            for scheduler in schedulers:
                await bot.send_message(chat_id=telegram_id, text=scheduler)

scheduler.add_job(
    notifying_student, 
    "interval",
    seconds=60, 
    kwargs={"bot": bot}
)


@student_handler.callback_query(F.data.in_("student_inline_keyboard_backward"))
async def student_inline_keyboard_backward(callback: CallbackQuery):
    """
    Обработчик нажатия кнопки "Назад" в меню обучающегося.

    Args:
        callback (CallbackQuery): Объект колбэка.

    Returns:
        None
    """
    await callback.message.edit_text(
        text="Панель обучающегося", reply_markup=inline_keyboard_panel
    )
    await callback.answer()


@student_handler.callback_query(F.data.in_("student_panel_cancel"))
async def student_panel_cancel(callback: CallbackQuery):
    """
    Обработчик отмены панели обучающегося.

    Args:
        callback (CallbackQuery): Объект колбэка.

    Returns:
        None
    """
    await callback.message.delete()
    await callback.answer()
