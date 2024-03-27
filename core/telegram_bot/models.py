from django.db import models


class Student(models.Model):
    "Ученики"
    telegram_id = models.PositiveBigIntegerField(
        verbose_name = 'Телеграм ID', 
        blank = True, 
        null = True, 
        unique = True, 
        db_index = True, 
        help_text = 'Указывается телеграм ID после аутентификации'
    )
    
    login = models.CharField(
        verbose_name = 'Логин в базе данных',
        max_length = 30,
        unique = True,
        blank = False,
        help_text = 'Укажите логин для ученика'
    )
    
    password = models.CharField(
        verbose_name = 'Пароль в базе данных',
        max_length = 30,
        blank = False,
        help_text = 'Укажите пароль для ученика'
    )
    
    full_name = models.CharField(
        verbose_name = 'ФИО',
        max_length = 45,
        unique = False,
        blank = False,
        help_text = 'Укажите ФИО ученика'
    )
    
    if_fourteen = models.BooleanField(
        verbose_name = 'Достиг ли ученик 14-го возраста',
        blank = False,
        default = False,
        help_text = 'Укажите достиг ли ученик 14-го возраста'
        
    )
    
    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return self.full_name