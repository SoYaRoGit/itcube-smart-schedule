from django.contrib import admin

from telegram_bot import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    """Регистрация модуля для учеников"""

    list_display = (
        "id",
        "full_name",
        "login",
        "password",
        "telegram_id",
        "is_authentication",
    )
    readonly_fields = ("telegram_id", "is_authentication")
    list_display_links = ["full_name"]


@admin.register(models.StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher")

    filter_horizontal = ["students"]
    list_display_links = ["name"]


@admin.register(models.StudentContentDetails)
class StudentContentDetailsAdmin(admin.ModelAdmin):
    """Регистрация модуля для персональных данных ученика"""

    list_display = (
        "id",
        "student",
        "parent_full_name",
        "parent_residential_adress",
        "date_birth",
        "if_fourteen",
        "student_residential_adress",
        "passport_data",
        "passport_data_issued_by",
        "passport_data_date_of_issueс",
        "name_education_organization",
        "certificate_number",
        "parent_contact",
        "student_contact",
        "medical_restrictions",
        "date_contract",
    )

    list_display_links = ["student"]


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Регистрация модуля для преподавателей"""

    list_display = (
        "id",
        "full_name",
        "login",
        "password",
        "telegram_id",
        "is_authentication",
    )
    readonly_fields = ("telegram_id", "is_authentication")
    list_display_links = ["full_name"]


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Регистрация модуля для дисциплин"""

    list_display = (
        "id",
        "name",
    )

    list_display_links = ["name"]


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """Регистрация модуля для учебных кабинетов"""

    list_display = ("id", "name")


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Регистрация модуля для занятий"""

    list_display = (
        "id",
        "date",
        "start_time",
        "end_time",
        "subject",
        "classroom",
        "group",
    )
