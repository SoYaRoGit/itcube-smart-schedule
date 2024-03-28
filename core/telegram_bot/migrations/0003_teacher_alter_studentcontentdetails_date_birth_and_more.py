# Generated by Django 4.2.1 on 2024-03-27 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_remove_student_if_fourteen_alter_student_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(help_text='Укажите логин для ученика', max_length=30, unique=True, verbose_name='Логин')),
                ('password', models.CharField(help_text='Укажите пароль для ученика', max_length=30, verbose_name='Пароль')),
                ('full_name', models.CharField(help_text='Укажите ФИО ученика', max_length=50, verbose_name='ФИО')),
                ('telegram_id', models.PositiveBigIntegerField(blank=True, db_index=True, help_text='Указывается телеграм ID после аутентификации', null=True, unique=True, verbose_name='Телеграм ID')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
            },
        ),
        migrations.AlterField(
            model_name='studentcontentdetails',
            name='date_birth',
            field=models.DateField(blank=True, help_text='Укажите дату рождения', verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='studentcontentdetails',
            name='name_education_organization',
            field=models.CharField(blank=True, help_text='Укажите название учебной организации', max_length=255, verbose_name='Учебная организация'),
        ),
        migrations.AlterField(
            model_name='studentcontentdetails',
            name='student_residential_adress',
            field=models.CharField(blank=True, help_text='Укажите адрес проживания с индексом', max_length=255, verbose_name='Адрес проживания'),
        ),
    ]