from django.contrib import admin
from telegram_bot import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    '''Регистрация модуля для учеников'''
    list_display = ('id', 
                    'full_name', 
                    'login', 
                    'password', 
                    'telegram_id'
    )
    
    list_display_links = ['full_name']
    
    
@admin.register(models.StudentContentDetails)
class StudentContentDetailsAdmin(admin.ModelAdmin):
    '''Регистрация модуля для персональных данных ученика'''

    list_display = ('id', 
                    'student', 
                    'parent_full_name', 
                    'parent_residential_adress', 
                    'date_birth', 
                    'if_fourteen', 
                    'student_residential_adress',
                    'passport_data', 
                    'passport_data_issued_by', 
                    'passport_data_date_of_issueс',
                    'name_education_organization', 
                    'certificate_number',
                    'parent_contact', 
                    'student_contact', 
                    'medical_restrictions', 
                    'date_contract'
    )
    
    list_display_links = ['student']


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    '''Регистрация модуля для преподавателей'''
    list_display = ('id', 
                    'full_name', 
                    'login', 
                    'password', 
                    'telegram_id'
    )
    
    list_display_links = ['full_name']