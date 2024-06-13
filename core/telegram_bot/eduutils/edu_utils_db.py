from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from telegram_bot.models import (
    Schedule,
    Student,
    StudentContentDetails,
    StudentGroup,
    Teacher,
)

TIME_BEFORE_STUDENT = settings.TIME_BEFORE_STUDENT
TIME_BEFORE_TEACHER = settings.TIME_BEFORE_TEACHER


def send_full_name(telegram_id: int) -> str:
    """
    Функция для получения полного имени пользователя по его telegram_id.

    Args:
        telegram_id (int): Идентификатор пользователя в Telegram.

    Returns:
        str: Полное имя пользователя (ФИО), если пользователь аутентифицирован, иначе пустая строка.
    """
    # Проверяем, существует ли студент с указанным telegram_id
    student_exists = Student.objects.filter(telegram_id=telegram_id).exists()

    # Если студент существует, проверяем его аутентификацию
    if student_exists:
        student = Student.objects.get(telegram_id=telegram_id)
        if student.is_authentication:
            return str(student.full_name)  # Если аутентифицирован, возвращаем ФИО

    # Если студент не найден или не аутентифицирован, проверяем преподавателя
    teacher_exists = Teacher.objects.filter(telegram_id=telegram_id).exists()
    if teacher_exists:
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        if teacher.is_authentication:
            return str(teacher.full_name)  # Если аутентифицирован, возвращаем ФИО

    return ""  # Если пользователь не аутентифицирован или не найден, возвращаем пустую строку


def not_authentication(telegram_id: int) -> bool:
    """
    Функция для проверки, аутентифицирован ли пользователь по его telegram_id.

    Args:
        telegram_id (int): Идентификатор пользователя в Telegram.

    Returns:
        bool: True, если пользователь не аутентифицирован, иначе False.
    """
    # Проверяем, существует ли студент с указанным telegram_id
    student_exists = Student.objects.filter(telegram_id=telegram_id).exists()

    # Если студент существует, проверяем его аутентификацию
    if student_exists:
        student = Student.objects.get(telegram_id=telegram_id)
        if student.is_authentication:
            return False  # Если аутентифицирован, возвращаем False

    # Если студент не найден или не аутентифицирован, проверяем преподавателя
    teacher_exists = Teacher.objects.filter(telegram_id=telegram_id).exists()
    if teacher_exists:
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        if teacher.is_authentication:
            return False  # Если аутентифицирован, возвращаем False

    # Если ни студент, ни преподаватель не найдены или не аутентифицированы, возвращаем True
    return True


def authentication_update(telegram_id: int, state_data: dict) -> bool:
    """
    Проводит аутентификацию студента или преподавателя на основе предоставленных данных.

    Args:
        telegram_id (int): Идентификатор Telegram пользователя.
        state_data (dict): Словарь данных, содержащий логин и пароль пользователя.

    Returns:
        bool: True, если пользователь успешно аутентифицирован, в противном случае False.
    """
    # Проверяем, существует ли студент с указанным логином, паролем
    student = Student.objects.filter(
        login=state_data["login"],
        password=state_data["password"],
        is_authentication=False,
    ).exists()

    # Если студент с такими данными существует, то проводим аутентификацию
    if student:
        Student.objects.filter(
            login=state_data["login"], password=state_data["password"]
        ).update(telegram_id=telegram_id, is_authentication=True)

        return True

    # Проверяем, существует ли преподаватель с указанным логином, паролем
    teacher = Teacher.objects.filter(
        login=state_data["login"],
        password=state_data["password"],
        is_authentication=False,
    ).exists()

    # Если преподаватель с такими данными существует, то проводим аутентификацию
    if teacher:
        Teacher.objects.filter(
            login=state_data["login"], password=state_data["password"]
        ).update(telegram_id=telegram_id, is_authentication=True)

        return True

    # В случае, если не найдены данные, то возвращаем False
    return False


def authentication_student(telegram_id: int) -> bool:
    """
    Проверяет аутентификацию студента по Telegram ID.

    Args:
        telegram_id (int): Идентификатор Telegram пользователя.

    Returns:
        bool: True, если студент аутентифицирован, иначе False.
    """
    # Проверяем, существует ли студент с указанным telegram_id
    student_exists = Student.objects.filter(telegram_id=telegram_id).exists()

    # Если студент существует, проверяем его аутентификацию
    if student_exists:
        student = Student.objects.get(telegram_id=telegram_id)
        if student.is_authentication:
            return True  # Если аутентифицирован, возвращаем True

    return False


def __student_to_dict_personal_data(student):
    """
    Преобразует объект студента в словарь с его персональными данными.

    Args:
        student: Объект студента.

    Returns:
        dict: Словарь с персональными данными студента.
            - id: Уникальный идентификатор студента.
            - login: Логин студента.
            - password: Пароль студента.
            - full_name: Полное имя студента.
            - telegram_id: Идентификатор Telegram студента.
            - is_authentication: Статус аутентификации студента.
    """
    return {
        "id": student.id,
        "login": student.login,
        "password": student.password,
        "full_name": student.full_name,
        "telegram_id": student.telegram_id,
        "is_authentication": student.is_authentication,
    }


def get_student_send_personal_data(telegram_id: int) -> dict:
    """
    Получает персональные данные студента по его Telegram ID.

    Args:
        telegram_id (int): Идентификатор Telegram студента.

    Returns:
        dict or None: Словарь с персональными данными студента, если студент найден,
            в противном случае возвращает None.
    """
    try:
        # Получить ученика по его Telegram ID
        student = Student.objects.get(telegram_id=telegram_id)
        # Преобразовать объект студента в словарь
        student_data = __student_to_dict_personal_data(student)
        return student_data
    except Student.DoesNotExist:
        # Обработка случая, когда студент с указанным telegram_id не найден
        return None


def __student_duct_confidential_data(student: Student) -> dict:
    """
    Преобразует объект студента в словарь с конфиденциальными данными.

    Args:
        student (Student): Объект студента.

    Returns:
        dict: Словарь с конфиденциальными данными студента.
    """
    return {
        "parent_full_name": student.parent_full_name,
        "parent_residential_adress": student.parent_residential_adress,
        "date_birth": student.date_birth,
        "if_fourteen": student.if_fourteen,
        "student_residential_adress": student.student_residential_adress,
        "passport_data": student.passport_data,
        "passport_data_issued_by": student.passport_data_issued_by,
        "passport_data_date_of_issueс": student.passport_data_date_of_issueс,
        "name_education_organization": student.name_education_organization,
        "certificate_number": student.certificate_number,
        "parent_contact": student.parent_contact,
        "student_contact": student.student_contact,
        "medical_restrictions": student.medical_restrictions,
        "date_contract": student.date_contract,
    }


def get_student_confidential_data(telegram_id: int) -> dict:
    """
    Получает конфиденциальные данные студента по его Telegram ID.

    Args:
        telegram_id (int): ID Telegram.

    Returns:
        dict: Словарь с конфиденциальными данными студента.
    """
    try:
        student = StudentContentDetails.objects.get(student__telegram_id=telegram_id)
        student_data = __student_duct_confidential_data(student)
        return student_data
    except Student.DoesNotExist:
        return None



def get_student_send_schedule(telegram_id: int) -> list[str]:
    """
    Получает расписание занятий для студента по его Telegram ID.

    Args:
        telegram_id (int): ID Telegram.

    Returns:
        list[str]: Список строковых представлений расписания занятий.
    """
    student = Student.objects.get(telegram_id=telegram_id)
    now = datetime.now()  # Получаем текущую дату и время

    # Фильтруем расписание по студенту и дате занятия, а также времени начала занятия
    schedules = (
        Schedule.objects.filter(
            Q(date=now.date(), end_time__gte=now.time())
            | Q(date__gt=now.date()),  # Начинающиеся после текущего времени
            group__students=student,
            date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
        )
        .order_by("date", "start_time")
        .all()
    )

    schedule_strings = [str(schedule) for schedule in schedules]

    return schedule_strings


def get_teacher_send_schedule(telegram_id: int) -> list[str]:
    """
    Получает расписание занятий для преподавателя по его Telegram ID.

    Args:
        telegram_id (int): ID Telegram преподавателя.

    Returns:
        list[str]: Список строковых представлений расписания занятий.
    """
    teacher = Teacher.objects.get(telegram_id=telegram_id)
    now = datetime.now()  # Получаем текущую дату и время

    # Фильтруем расписание по преподавателю и дате занятия, а также времени начала занятия
    schedules = (
        Schedule.objects.filter(
            Q(date=now.date(), end_time__gte=now.time())
            | Q(date__gt=now.date()),  # Начинающиеся после текущего времени
            group__teacher=teacher,
            date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
        )
        .order_by("date", "start_time")
        .all()
    )

    schedule_strings = [str(schedule) for schedule in schedules]

    return schedule_strings


def student_send_schedule_reminder() -> dict[int, list[str]]:
    """
    Отправляет напоминания об учебном расписании для студентов.

    Returns:
        dict[int, list[str]]: Словарь, где ключ - ID Telegram студента, а значение - список строковых представлений расписания.
    """
    time_now = datetime.now().replace(
        second=0, microsecond=0
    )  # Получаем текущую дату и время

    students = Student.objects.all()

    students_schedule = {}

    for student in students:
        schedules = (
            Schedule.objects.filter(
                date=time_now.date(),  # Занятия только на сегодняшний день
                group__students=student,
                end_time__gte=time_now.time(),  # Занятия до момента их окончания
            )
            .order_by("date", "start_time")
            .all()
        )

        schedule_strings = []

        for schedule in schedules:
            start_datetime = timezone.datetime.combine(
                schedule.date, schedule.start_time
            )
            end_datetime = timezone.datetime.combine(schedule.date, schedule.end_time)

            if time_now == start_datetime - timedelta(minutes=TIME_BEFORE_STUDENT):
                schedule_strings.append(
                    f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )

            if time_now == start_datetime:
                schedule_strings.append(
                    f"[Начало занятия]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )

            if time_now == end_datetime:
                schedule_strings.append(
                    f"[Оповещение о завершении]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )
                schedule.delete()
        students_schedule[student.telegram_id] = schedule_strings

    return students_schedule


def teacher_send_schedule_reminder() -> dict[int, list[str]]:
    """
    Отправляет напоминания об учебном расписании для преподавателей.

    Returns:
        dict[int, list[str]]: Словарь, где ключ - ID Telegram преподавателя, а значение - список строковых представлений расписания.
    """
    time_now = datetime.now().replace(
        second=0, microsecond=0
    )  # Получаем текущую дату и время

    teachers = Teacher.objects.all()

    teachers_schedule = {}

    for teacher in teachers:
        schedules = (
            Schedule.objects.filter(
                date=time_now.date(),  # Занятия только на сегодняшний день
                group__teacher=teacher,
                end_time__gte=time_now.time(),  # Занятия до момента их окончания
            )
            .order_by("date", "start_time")
            .all()
        )

        schedule_strings = []

        for schedule in schedules:
            start_datetime = timezone.datetime.combine(
                schedule.date, schedule.start_time
            )
            end_datetime = timezone.datetime.combine(schedule.date, schedule.end_time)

            if time_now == start_datetime - timedelta(minutes=TIME_BEFORE_TEACHER):
                schedule_strings.append(
                    f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )

            if time_now == start_datetime:
                schedule_strings.append(
                    f"[Начало занятия]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )

            if time_now == end_datetime:
                schedule_strings.append(
                    f"[Оповещение о завершении]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}"
                )
                schedule.delete()
        teachers_schedule[teacher.telegram_id] = schedule_strings

    return teachers_schedule


def __teacher_to_dict(teacher: Teacher) -> dict:
    """
    Преобразует объект преподавателя в словарь.

    Args:
        teacher (Teacher): Объект преподавателя.

    Returns:
        dict: Словарь с данными преподавателя.
    """
    return {
        "id": teacher.id,
        "login": teacher.login,
        "password": teacher.password,
        "full_name": teacher.full_name,
        "telegram_id": teacher.telegram_id,
        "is_authentication": teacher.is_authentication,
    }


def get_teacher_send_personal_data(telegram_id: int) -> dict:
    """
    Получает персональные данные преподавателя по его Telegram ID.

    Args:
        telegram_id (int): ID Telegram.

    Returns:
        dict: Словарь с персональными данными преподавателя, если найден, иначе None.
    """
    try:
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        teacher_data = __teacher_to_dict(teacher)
        return teacher_data
    except Teacher.DoesNotExist:
        return None


def get_students_group_telegram_id(name_group: str) -> list:
    """
    Получает список Telegram ID студентов определенной группы.

    Args:
        name_group (str): Название группы.

    Returns:
        list: Список Telegram ID студентов в указанной группе, если найдены, иначе None.
    """
    try:
        students_telegram_id = []
        students = Student.objects.filter(
            studentgroup__name=name_group, is_authentication=True
        )

        for student in students:
            students_telegram_id.append(student.telegram_id)

        return students_telegram_id
    except Student.DoesNotExist:
        return None


def get_students_group_full_name(name_group: str) -> list[str]:
    """
    Получает список полных имен студентов определенной группы.

    Args:
        name_group (str): Название группы.

    Returns:
        list[str] or None: Список полных имен студентов в указанной группе, если найдены, иначе None.
    """
    try:
        students_name = []
        students = Student.objects.filter(
            studentgroup__name=name_group, is_authentication=True
        )

        for student in students:
            students_name.append(student.full_name)

        return students_name
    except Student.DoesNotExist:
        return None


def get_groups_teacher(telegram_id_teacher: int) -> list[tuple]:
    """
    Получает список групп, преподаваемых определенным преподавателем.

    Args:
        telegram_id_teacher (int): Telegram ID преподавателя.

    Returns:
        list[tuple]: Список кортежей (название группы, строковое представление группы).
    """
    groups = StudentGroup.objects.filter(teacher__telegram_id=telegram_id_teacher)
    teacher_groups = [(group.name, str(group)) for group in groups]
    return teacher_groups


def authentication_teacher(telegram_id: int) -> bool:
    """
    Проверяет аутентификацию преподавателя по его Telegram ID.

    Args:
        telegram_id (int): Идентификатор Telegram пользователя.

    Returns:
        bool: True, если преподаватель аутентифицирован, иначе False.
    """
    teacher_exists = Teacher.objects.filter(telegram_id=telegram_id).exists()
    if teacher_exists:
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        if teacher.is_authentication:
            return True
    return False
