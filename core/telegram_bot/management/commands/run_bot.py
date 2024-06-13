from asyncio import run
from typing import Any

from django.core.management.base import BaseCommand

from telegram_bot.bot import main


class Command(BaseCommand):
    """
    Django команда для запуска телеграм бота.

    Команда запускает функцию main() из модуля telegram_bot.bot в асинхронном режиме.

    Attributes:
    - args: Позиционные аргументы команды.
    - options: Дополнительные опции команды.

    Methods:
    - handle: Метод для обработки команды. Запускает функцию main() в асинхронном режиме.
    
    Returns:
    - str | None: Строка или None в зависимости от результата выполнения.
    """
    def handle(self, *args: Any, **options: Any) -> str | None:
        """
        Метод для обработки команды. Запускает функцию main() в асинхронном режиме.

        Args:
        - args: Позиционные аргументы команды.
        - options: Дополнительные опции команды.

        Returns:
        - str | None: Строка или None в зависимости от результата выполнения.
        """
        run(main())
