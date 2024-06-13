from aiogram import Bot, F, Router, html
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from telegram_bot.eduutils.edu_utils_db import (
    get_teacher_send_personal_data,
    get_teacher_send_schedule,
    teacher_send_schedule_reminder,
)
from telegram_bot.filters.filter import AuthenticationTeacherFilter
from telegram_bot.keyboards.teacher_keyboard import (
    builder_inline_keyboard_group,
    inline_keyboard_backward,
    inline_keyboard_panel,
)
from telegram_bot.loader import bot, scheduler
from telegram_bot.states.teacher_message_state import teacher_message_state_router

# Создание роутера для обработки сообщений преподавателей
teacher_handler = Router()

# Включение внутреннего роутера для обработки состояний отправки сообщений преподавателя
teacher_handler.include_router(teacher_message_state_router)

# Установка фильтра, разрешающего только аутентифицированным преподавателям обращаться к обработчикам
teacher_handler.message(AuthenticationTeacherFilter())


@teacher_handler.message(F.text == "/panel", AuthenticationTeacherFilter())
async def cmd_panel_teacher(message: Message):
    """
    Обработчик команды "/panel" для преподавателей.

    Удаляет сообщение с командой и отправляет сообщение с панелью преподавателя, используя клавиатуру inline_keyboard_panel.

    Args:
        message (Message): Входящее сообщение.

    Returns:
        None
    """
    await message.delete()
    await message.answer(
        text="Панель преподавателя",
        reply_markup=inline_keyboard_panel,
        protect_content=True,
    )


@teacher_handler.callback_query(F.data.in_("teacher_send_personal_data"))
async def teacher_send_personal_data(callback: CallbackQuery):
    """
    Обработчик коллбэк-кнопки "teacher_send_personal_data" для преподавателей.

    Извлекает персональные данные преподавателя из базы данных и отображает их в сообщении.

    Args:
        callback (CallbackQuery): CallbackQuery объект.

    Returns:
        None
    """
    personal_data = await sync_to_async(get_teacher_send_personal_data)(
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


@teacher_handler.callback_query(F.data.in_("teacher_send_schedule"))
async def teacher_send_schedule(callback: CallbackQuery):
    """
    Обработчик коллбэк-кнопки "teacher_send_schedule" для преподавателей.

    Отправляет преподавателю расписание занятий.

    Args:
        callback (CallbackQuery): CallbackQuery объект.

    Returns:
        None
    """
    schedule = await sync_to_async(get_teacher_send_schedule)(callback.from_user.id)
    if schedule:
        await callback.message.answer(text="\n".join(str(item) for item in schedule))
    else:
        await callback.message.answer(
            text="В данный момент нет запланированных занятий"
        )

    await callback.answer()


async def notifying_teachers(bot: Bot):
    """
    Асинхронная функция для отправки напоминаний преподавателям о предстоящих занятиях.

    Args:
        bot (Bot): Объект бота.

    Returns:
        None
    """
    reminder = await sync_to_async(teacher_send_schedule_reminder)()

    for telegram_id, schedulers in reminder.items():
        if schedulers:
            for scheduler in schedulers:
                await bot.send_message(chat_id=telegram_id, text=scheduler)

scheduler.add_job(
    notifying_teachers,
    "interval",
    seconds=60,
    kwargs={"bot": bot}
)


@teacher_handler.callback_query(F.data.in_("teacher_send_message_for_group"))
async def teacher_send_message_for_group(callback: CallbackQuery):
    """
    Обработчик коллбэк-кнопки "teacher_send_message_for_group" для отправки сообщений преподавателем всей группе.

    Args:
        callback (CallbackQuery): CallbackQuery объект.

    Returns:
        None
    """
    keyboard = await builder_inline_keyboard_group(callback.from_user.id)
    await callback.message.edit_text(
        text="Выберите группу для отправки сообщения", reply_markup=keyboard
    )
    await callback.answer()


@teacher_handler.callback_query(F.data.in_("teacher_inline_keyboard_backward"))
async def teacher_inline_keyboard_backward(callback: CallbackQuery):
    """
    Обработчик коллбэк-кнопки "teacher_inline_keyboard_backward" для возврата к панели преподавателя.

    Args:
        callback (CallbackQuery): CallbackQuery объект.

    Returns:
        None
    """
    await callback.message.edit_text(
        text="Панель преподавателя", reply_markup=inline_keyboard_panel
    )
    await callback.answer()


@teacher_handler.callback_query(F.data.in_("teacher_panel_cancel"))
async def teacher_panel_cancel(callback: CallbackQuery):
    """
    Обработчик коллбэк-кнопки "teacher_panel_cancel" для отмены панели преподавателя.

    Args:
        callback (CallbackQuery): CallbackQuery объект.

    Returns:
        None
    """
    await callback.message.delete()
    await callback.answer()
