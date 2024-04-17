from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from telegram_bot.eduutils.edu_utils_db import (
    authentication_student,
    authentication_teacher,
    authentication_update,
    get_groups_teacher,
    not_authentication,
)


class NotAuthenticationFilter(BaseFilter):
    """
    Фильтр для проверки, аутентифицирован ли пользователь.

    Args:
        BaseFilter: Базовый класс для создания пользовательских фильтров.

    Returns:
        bool: True, если пользователь не аутентифицирован, иначе False.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверка, аутентифицирован ли пользователь по его telegram_id.

        Args:
            message (Message): Объект сообщения пользователя.

        Returns:
            bool: True, если пользователь не аутентифицирован, иначе False.
        """
        telegram_id = message.from_user.id
        return await sync_to_async(not_authentication)(telegram_id)


class AuthenticationUpdateFilter(BaseFilter):
    """
    Фильтр для проверки возможности обновления данных аутентификации.

    Args:
        BaseFilter: Базовый класс для фильтров aiogram.

    Returns:
        bool: True, если обновление данных аутентификации возможно, иначе False.
    """

    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> bool:
        """
        Проверяет возможность обновления данных аутентификации.

        Args:
            callback (CallbackQuery): CallbackQuery объект.
            state (FSMContext): Контекст конечного автомата.

        Returns:
            bool: True, если обновление данных аутентификации возможно, иначе False.
        """
        telegram_id = callback.from_user.id
        state_data = await state.get_data()
        return await sync_to_async(authentication_update)(telegram_id, state_data)


class AuthenticationStudentFilter(BaseFilter):
    """
    Фильтр для проверки аутентификации студента.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет аутентификацию студента по Telegram ID.

        Args:
            message (Message): Объект сообщения.

        Returns:
            bool: True, если студент аутентифицирован, иначе False.
        """
        telegram_id: int = message.from_user.id
        return await sync_to_async(authentication_student)(telegram_id)


class AuthenticationTeacherFilter(BaseFilter):
    """
    Фильтр для проверки аутентификации преподавателя.

    Attributes:
        message (Message): Сообщение, полученное от пользователя.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет аутентификацию преподавателя по Telegram ID.

        Args:
            message (Message): Сообщение, полученное от пользователя.

        Returns:
            bool: True, если преподаватель аутентифицирован, иначе False.
        """
        telegram_id: int = message.from_user.id
        return await sync_to_async(authentication_teacher)(telegram_id)


class CallbackTeacherGroupsFilter(BaseFilter):
    """
    Фильтр для проверки сообщений от преподавателя по группам.

    Attributes:
        callback (CallbackQuery): Обратный вызов (callback), полученный от пользователя.
    """

    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        """
        Проверяет, принадлежит ли данные callback одной из групп преподавателя.

        Args:
            callback (CallbackQuery): Обратный вызов (callback), полученный от пользователя.

        Returns:
            Union[bool, dict[str, str]]: False, если callback не принадлежит ни одной группе преподавателя,
                в противном случае возвращает словарь с информацией о группе, в которой находится callback.
        """
        teacher_groups: list[tuple[str]] = await sync_to_async(get_groups_teacher)(
            callback.from_user.id
        )

        for group_tuple in teacher_groups:
            if callback.data in group_tuple:
                return {"group": group_tuple[0]}  # Возвращаем первый элемент кортежа

        return False
