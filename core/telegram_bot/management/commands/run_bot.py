from asyncio import run
from django.core.management.base import BaseCommand
from telegram_bot.bot import main
from typing import Any



class Command(BaseCommand):    
    def handle(self, *args: Any, **options: Any) -> str | None:
        run(main())