from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.methods import EditMessageText
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from telegram_bot.filters.filter import (
    AuthenticationUpdateFilter,
    NotAuthenticationFilter,
    send_full_name,
)
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication,
    inline_keyboard_authentication_cancel,
    inline_keyboard_authentication_check,
)
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.loader import bot

# Создание роутера для обработки состояний аутентификации
authentication_state_router = Router()


async def send_update_message(
    chat_id, message_id, text, keyboard=inline_keyboard_authentication_cancel
) -> EditMessageText:
    """
    Асинхронная функция для отправки обновленного сообщения с возможностью изменения текста и клавиатуры.

    Parameters:
    - chat_id: Идентификатор чата, в который отправляется сообщение.
    - message_id: Идентификатор сообщения, которое необходимо обновить.
    - text: Текст для обновления сообщения.
    - keyboard: Клавиатура для обновленного сообщения. По умолчанию используется клавиатура inline_keyboard_authentication_cancel.

    Returns:
    - Изменяет текст и клавиатуру
    """
    # Отправка запроса на изменение текста и клавиатуры сообщения
    await bot(
        EditMessageText(
            text=text, chat_id=chat_id, message_id=message_id, reply_markup=keyboard
        )
    )


class FSMAuthenticationForm(StatesGroup):
    """
    Группа состояний для формы аутентификации.

    States:
    - LOGIN: Состояние для ввода логина.
    - PASSWORD: Состояние для ввода пароля.
    """

    LOGIN = State()
    PASSWORD = State()


@authentication_state_router.callback_query(
    F.data.in_("authentication_state_cancel"), ~StateFilter(default_state)
)
async def authentication_state_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для отмены аутентификации.

    Args:
    - callback (CallbackQuery): CallbackQuery объект.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Редактирование сообщения с предложением начать аутентификацию снова
    await callback.message.edit_text(
        text=AUTHENTICATION_TEXT["cmd_start_not_authentication"].format(
            callback.from_user.full_name
        ),
        reply_markup=inline_keyboard_authentication,
    )

    # Очистка состояния FSM
    await state.clear()

    # Отправка подтверждения ответа на callback-запрос
    await callback.answer()


@authentication_state_router.callback_query(F.data.in_("authentication_state_login"))
async def authentication_continue(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для продолжения процесса аутентификации с вводом логина.

    Args:
    - callback (CallbackQuery): CallbackQuery объект.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Редактирование сообщения с просьбой ввести логин
    await callback.message.edit_text(
        text=AUTHENTICATION_TEXT["authentication_state_login"],
        reply_markup=inline_keyboard_authentication_cancel,
    )

    # Запоминание ID чата и ID сообщения для последующего обновления
    await state.update_data(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id
    )

    # Установка состояния FSM для ввода логина
    await state.set_state(state=FSMAuthenticationForm.LOGIN)

    # Отправка подтверждения ответа на callback-запрос
    await callback.answer()


@authentication_state_router.message(StateFilter(FSMAuthenticationForm.LOGIN))
async def state_input_login(message: Message, state: FSMContext):
    """
    Обработчик для ввода логина в процессе аутентификации.

    Args:
    - message (Message): Message объект с текстом введенного логина.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Удаление сообщения с введенным логином
    await message.delete()

    # Обновление данных состояния с сохранением введенного логина
    await state.update_data(login=message.text)

    # Получение данных из состояния
    data = await state.get_data()

    # Отправка обновленного сообщения с просьбой ввести пароль
    await send_update_message(
        chat_id=data["chat_id"],
        message_id=data["message_id"],
        text=AUTHENTICATION_TEXT["authentication_state_password"],
    )

    # Установка состояния FSM для ввода пароля
    await state.set_state(state=FSMAuthenticationForm.PASSWORD)


@authentication_state_router.message(StateFilter(FSMAuthenticationForm.PASSWORD))
async def state_input_password(message: Message, state: FSMContext):
    """
    Обработчик для ввода пароля в процессе аутентификации.

    Args:
    - message (Message): Message объект с текстом введенного пароля.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Удаление сообщения с введенным паролем
    await message.delete()

    # Обновление данных состояния с сохранением введенного пароля
    await state.update_data(
        password=message.text
    )

    # Получение данных из состояния
    data = await state.get_data()

    # Форматирование текста с данными аутентификации
    authentication_data = AUTHENTICATION_TEXT["authentication_data"].format(
        data["login"], data["password"]
    )

    # Отправка обновленного сообщения с данными аутентификации и клавиатурой для подтверждения
    await send_update_message(
        chat_id=data["chat_id"],
        message_id=data["message_id"],
        text=authentication_data,
        keyboard=inline_keyboard_authentication_check,
    )


@authentication_state_router.callback_query(
    F.data.in_("authentication_check"), AuthenticationUpdateFilter()
)
async def state_authentication_check(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для вывода информации о успешной авторизации.

    Args:
    - callback (CallbackQuery): CallbackQuery объект.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Получение данных из состояния
    data = await state.get_data()

    # Форматирование текста ответа с аутентификационными данными
    response_text = AUTHENTICATION_TEXT["authentication_check"].format(
        await sync_to_async(send_full_name)(callback.from_user.id),
        data["login"],
        data["password"],
    )

    # Отправка ответа с аутентификационными данными в виде всплывающего уведомления
    await callback.answer(text=response_text, show_alert=True)

    # Очистка состояния FSM
    await state.clear()

    # Удаление сообщения с запросом аутентификации
    await callback.message.delete()


@authentication_state_router.callback_query(
    F.data.in_("authentication_check"), ~AuthenticationUpdateFilter()
)
async def state_not_authentication_check(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для вывода информации о безуспешной авторизации.

    Args:
    - callback (CallbackQuery): CallbackQuery объект.
    - state (FSMContext): Контекст состояния для управления состояниями в FSM.

    Returns:
    - None
    """
    # Получение данных из состояния
    data = await state.get_data()

    # Форматирование текста ответа с аутентификационными данными
    response_text = AUTHENTICATION_TEXT["not_authentication_check"].format(
        await sync_to_async(send_full_name)(callback.from_user.id),
        data["login"],
        data["password"],
    )

    # Отправка ответа с аутентификационными данными в виде всплывающего уведомления
    await callback.answer(text=response_text, show_alert=True)

    # Очистка состояния FSM
    await state.clear()

    # Удаление сообщения с запросом аутентификации
    await callback.message.delete()


@authentication_state_router.message(NotAuthenticationFilter())
async def not_authentication_user(message: Message):
    """
    Обработчик для сообщений от пользователей, не прошедших аутентификацию.

    Args:
    - message (Message): Message объект.

    Returns:
    - None
    """
    # Удаление сообщения
    await message.delete()
    # Отправка сообщения с предложением пройти аутентификацию
    await message.answer(text="Вы не прошли аутентификацию, пожалуйста пройдите /start")
