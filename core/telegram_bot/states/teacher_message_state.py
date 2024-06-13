from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from telegram_bot.eduutils.edu_utils_db import (
    get_students_group_full_name,
    get_students_group_telegram_id,
)
from telegram_bot.filters.filter import CallbackTeacherGroupsFilter
from telegram_bot.keyboards.teacher_message_state_keyboard import (
    inline_keyboard_teacher_message_state_menu,
)
from telegram_bot.loader import bot

# Создание роутера для обработки состояний сообщений преподавателя
teacher_message_state_router = Router()

# Определение группы состояний для формы отправки сообщения преподавателя
class FSMTeacherSendMessageForm(StatesGroup):
    MESSAGE = State()


@teacher_message_state_router.callback_query(CallbackTeacherGroupsFilter())
async def teacher_message_state_start(
    callback: CallbackQuery, group: str, state: FSMContext
):
    """
    Обработчик для начала отправки сообщения преподавателем.

    Args:
        callback (CallbackQuery): CallbackQuery объект.
        group (str): Название группы, для которой отправляется сообщение.
        state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
        Список групп закрепленных за преподавателем
    """
    # Получение полного списка студентов в выбранной группе
    student_name = await sync_to_async(get_students_group_full_name)(group)

    # Обновление данных в состоянии FSM
    await state.update_data(
        name_group=group, 
        student_names=student_name
    )

    # Редактирование сообщения с запросом подтверждения выбора группы
    await callback.message.edit_text(
        text=f"Подтвердите выбор выбранной группы: {group}",
        reply_markup=inline_keyboard_teacher_message_state_menu,
    )

    # Отправка ответа на callback-запрос
    await callback.answer()


@teacher_message_state_router.callback_query(
    F.data.in_("teacher_message_state_menu_confirm")
)
async def teacher_message_state_menu_confirm(
    callback: CallbackQuery, state: FSMContext
):
    """
    Обработчик для подтверждения выбора группы преподавателем.

    Args:
        callback (CallbackQuery): CallbackQuery объект.
        state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
        Выбранную группу учеников преподавателем
    """
    # Получение данных из состояния FSM
    data = await state.get_data()

    # Получение информации о группе и студентах
    group_name = data.get("name_group", "")
    student_names = data.get("student_names", [])

    # Создание строки с именами студентов
    student_names_str = ", ".join(student_names)

    # Формирование текста сообщения
    message_text = (
        f"Вы успешно выбрали группу: {group_name}\n\n"
        f"Студенты, которые будут уведомлены:\n{student_names_str}"
    )

    # Установка состояния FSM для отправки сообщения
    await state.set_state(state=FSMTeacherSendMessageForm.MESSAGE)

    # Отправка сообщения
    await callback.message.answer(message_text)


@teacher_message_state_router.message(StateFilter(FSMTeacherSendMessageForm.MESSAGE))
async def FSMTeacherSendMessageForm_MESSAGE(message: Message, state: FSMContext):
    """
    Обработчик для отправки сообщения преподавателем.

    Args:
        message (Message): Message объект с текстом сообщения.
        state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
        Сообщение для определенной группе учеников
    """
    # Получение данных из состояния FSM
    data = await state.get_data()

    # Получение списка telegram_id студентов выбранной группы
    telegram_ids = await sync_to_async(get_students_group_telegram_id)(
        data["name_group"]
    )

    # Отправка сообщения каждому студенту
    for telegram_id in telegram_ids:
        await bot.send_message(
            chat_id=telegram_id, text=f"[ОПОВЕЩЕНИЕ]\n{message.text}"
        )

    # Отправка подтверждения отправки сообщения преподавателю
    await message.answer(
        text=f'Вы успешно отправили сообщение группе: {data["name_group"]}'
    )

    # Очистка состояния FSM
    await state.clear()
