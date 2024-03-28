# Generated by Django 4.2.1 on 2024-03-28 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0009_studentgroup_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Укажите дату занятия', verbose_name='Дата занятия')),
                ('start_time', models.TimeField(help_text='Укажите время начала занятия', verbose_name='Время начала занятия')),
                ('end_time', models.TimeField(help_text='Укажите время окончания занятия', verbose_name='Время окончания занятия')),
                ('classroom', models.ForeignKey(help_text='Укажите кабинет', on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.classroom', verbose_name='Кабинет')),
                ('group', models.ForeignKey(help_text='Укажите группу', on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.studentgroup', verbose_name='Группа')),
                ('subject', models.ForeignKey(help_text='Укажите дисциплину', on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.subject', verbose_name='Дисциплина')),
            ],
        ),
    ]