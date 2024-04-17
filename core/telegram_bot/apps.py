from django.apps import AppConfig

class TelegramBotConfig(AppConfig):
    """
    Конфигурация приложения телеграм-бота.

    Attributes:
        default_auto_field (str): Имя поля для автоматического установки первичного ключа.
        name (str): Имя приложения.
        verbose_name (str): Отображаемое имя приложения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"
    verbose_name = "Телеграм Бот"