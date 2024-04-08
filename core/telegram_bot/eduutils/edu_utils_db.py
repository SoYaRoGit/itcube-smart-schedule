from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from telegram_bot.models import Student, Schedule, Teacher
from datetime import timedelta


def __student_to_dict(student):
    return {
        'id': student.id,
        'login': student.login,
        'password': student.password,
        'full_name': student.full_name,
        'telegram_id': student.telegram_id,
        'is_authentication': student.is_authentication,
    }

def get_student_send_personal_data(telegram_id):
    try:
        # Получить ученика по его Telegram ID
        student = Student.objects.get(telegram_id=telegram_id)
        # Преобразовать объект студента в словарь
        student_data = __student_to_dict(student)
        return student_data
    except Student.DoesNotExist:
        # Обработка случая, когда студент с указанным telegram_id не найден
        return None


def get_student_send_schedule(telegram_id: int):
    student = Student.objects.get(telegram_id=telegram_id)
    now = datetime.now()  # Получаем текущую дату и время
    
    # Фильтруем расписание по студенту и дате занятия, а также времени начала занятия
    schedules = Schedule.objects.filter(
        Q(date=now.date(), start_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
        group__students=student,
        date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
    ).order_by('date', 'start_time').all()
    
    schedule_strings = [str(schedule) for schedule in schedules]
    
    return schedule_strings


def get_teacher_send_schedule(telegram_id: int):
    teacher = Teacher.objects.get(telegram_id=telegram_id)
    now = datetime.now()  # Получаем текущую дату и время
    
    # Фильтруем расписание по студенту и дате занятия, а также времени начала занятия
    schedules = Schedule.objects.filter(
        Q(date=now.date(), start_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
        group__teacher=teacher,
        date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
    ).order_by('date', 'start_time').all()
    
    schedule_strings = [str(schedule) for schedule in schedules]
    
    return schedule_strings


def student_send_schedule_reminder():
    now = datetime.now()  # Получаем текущую дату и время
    notification_time = now + timedelta(minutes=1) # Время оповещения 
    
    students = Student.objects.all()
    
    students_schedule = {}
    
    for student in students:
        schedules = Schedule.objects.filter(
            Q(date=now.date(), start_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
            group__students=student,
            date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
        ).order_by('date', 'start_time').all()
        
        schedule_strings = []
        
        for schedule in schedules:
            start_datetime = timezone.datetime.combine(schedule.date, schedule.start_time)
            # Проверяем, находится ли текущее время за 30 минут до начала занятия
            if notification_time >= start_datetime >= now:
                # Если условие выполняется, добавляем информацию о занятии в список для оповещения
                schedule_strings.append(f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")

        students_schedule[student.telegram_id] = schedule_strings
    
    return students_schedule


def teacher_send_schedule_reminder():
    now = datetime.now()  # Получаем текущую дату и время
    notification_time = now + timedelta(minutes=1) # Время оповещения 
    
    teachers = Teacher.objects.all()
    
    teachers_schedule = {}
    
    for teacher in teachers:
        schedules = Schedule.objects.filter(
            Q(date=now.date(), start_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
            group__teacher=teacher,
            date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
        ).order_by('date', 'start_time').all()
        
        schedule_strings = []
        
        for schedule in schedules:
            start_datetime = timezone.datetime.combine(schedule.date, schedule.start_time)
            # Проверяем, находится ли текущее время за 30 минут до начала занятия
            if notification_time >= start_datetime >= now:
                # Если условие выполняется, добавляем информацию о занятии в список для оповещения
                schedule_strings.append(f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")
                schedule.delete()  # Удалить только текущее занятие из базы данных


        teachers_schedule[teacher.telegram_id] = schedule_strings
    
    return teachers_schedule


def __teacher_to_dict(teacher):
    return {
        'id': teacher.id,
        'login': teacher.login,
        'password': teacher.password,
        'full_name': teacher.full_name,
        'telegram_id': teacher.telegram_id,
        'is_authentication': teacher.is_authentication,
    }

def get_teacher_send_personal_data(telegram_id):
    try:
        # Получить ученика по его Telegram ID
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        # Преобразовать объект студента в словарь
        teacher_data = __teacher_to_dict(teacher)
        return teacher_data
    except Student.DoesNotExist:
        # Обработка случая, когда студент с указанным telegram_id не найден
        return None