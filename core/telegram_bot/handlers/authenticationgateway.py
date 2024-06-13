from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from telegram_bot.filters.filter import NotAuthenticationFilter
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication,
    inline_keyboard_authentication_menu,
)
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.states.authentication_state import authentication_state_router

# Создание роутера для обработки запросов аутентификации
authentication_router = Router()

# Включение в роутер обработчиков состояний аутентификации
authentication_router.include_router(authentication_state_router)


# Добавление обработчика для команды /start для неаутентифицированных пользователей
@authentication_router.message(CommandStart(), NotAuthenticationFilter())
async def cmd_start(message: Message):
    """
    Обработчик команды /start для неаутентифицированных пользователей.

    Удаляет сообщение /start и отправляет стартовое сообщение с предложением авторизации.

    Args:
        message (Message): Полученное сообщение.

    Returns:
        None
    """
    await message.delete()
    await message.answer(
        text=AUTHENTICATION_TEXT["cmd_start_not_authentication"].format(
            message.from_user.full_name
        ),
        reply_markup=inline_keyboard_authentication,  # Кнопка с предложением авторизации
    )


# Добавление обработчика для нажатия кнопки авторизации
@authentication_router.callback_query(F.data.in_("authentication"))
async def authentication_menu(callback: CallbackQuery):
    """
    Обработчик нажатия кнопки авторизации.

    Изменяет текст сообщения на меню аутентификации.

    Args:
        callback (CallbackQuery): Объект callback запроса.

    Returns:
        None
    """
    await callback.message.edit_text(
        text=AUTHENTICATION_TEXT["authentication_menu"],  # Текст меню аутентификации
        reply_markup=inline_keyboard_authentication_menu,  # Клавиатура с опциями аутентификации
    )

    await callback.answer()  # Подтверждение выполнения действия


# Добавление обработчика для нажатия кнопки "Назад" в меню аутентификации
@authentication_router.callback_query(F.data.in_("authentication_backward"))
async def authentication_backward(callback: CallbackQuery):
    """
    Обработчик нажатия кнопки "Назад" в меню аутентификации.

    Изменяет текст сообщения на стартовое сообщение для не аутентифицированных пользователей.

    Args:
        callback (CallbackQuery): Объект callback запроса.

    Returns:
        None
    """
    await callback.message.edit_text(
        text=AUTHENTICATION_TEXT["cmd_start_not_authentication"].format(
            callback.from_user.full_name
        ),  # Текст стартового сообщения для не аутентифицированных пользователей
        reply_markup=inline_keyboard_authentication,  # Клавиатура с кнопкой аутентификации
    )
    await callback.answer()  # Подтверждение выполнения действия
