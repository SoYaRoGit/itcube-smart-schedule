# Generated by Django 4.2.1 on 2024-03-28 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0005_studentgroup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentgroup',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='students',
            field=models.ManyToManyField(to='telegram_bot.student', verbose_name='В каких группах состоит ученик'),
        ),
    ]
