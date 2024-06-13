from typing import Any
from django.core.management.base import BaseCommand
from cryptography.fernet import Fernet



class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        print(f'Ключ: {Fernet.generate_key()}')
