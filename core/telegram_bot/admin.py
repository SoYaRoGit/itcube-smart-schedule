from django.contrib import admin
from telegram_bot import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    '''Регистрация модуля для учеников'''

    list_display = ('id', 'full_name', 'login', 'password', 'telegram_id', 'if_fourteen')