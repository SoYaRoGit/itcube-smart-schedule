from django.contrib import admin

from telegram_bot import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Регистрация модели учеников для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов учеников.
        readonly_fields (tuple): Список полей, доступных только для чтения в административной панели.
        list_display_links (list): Список полей, которые являются ссылками на страницы редактирования объектов.
    """

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
    """
    Регистрация модели группы учеников для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов группы учеников.
        filter_horizontal (list): Список полей, для которых будет использоваться фильтр с возможностью множественного выбора.
        list_display_links (list): Список полей, которые являются ссылками на страницы редактирования объектов.
    """

    list_display = ("id", "name", "teacher")
    filter_horizontal = ["students"]
    list_display_links = ["name"]


@admin.register(models.StudentContentDetails)
class StudentContentDetailsAdmin(admin.ModelAdmin):
    """
    Регистрация модели персональных данных ученика для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов персональных данных ученика.
        list_display_links (list): Список полей, которые являются ссылками на страницы редактирования объектов.
    """

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
    """
    Регистрация модели преподавателей для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов преподавателей.
        readonly_fields (tuple): Список полей, доступных только для чтения в административной панели.
        list_display_links (list): Список полей, которые являются ссылками на страницы редактирования объектов.
    """

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
    """
    Регистрация модели дисциплин для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов дисциплин.
        list_display_links (list): Список полей, которые являются ссылками на страницы редактирования объектов.
    """

    list_display = ("id", "name")
    list_display_links = ["name"]


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """
    Регистрация модели учебных кабинетов для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов учебных кабинетов.
    """

    list_display = ("id", "name")


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """
    Регистрация модели занятий для административной панели Django.

    Attributes:
        list_display (tuple): Список полей, отображаемых в списке объектов занятий.
    """

    list_display = (
        "id",
        "date",
        "start_time",
        "end_time",
        "subject",
        "classroom",
        "group",
    )
