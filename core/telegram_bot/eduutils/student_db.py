from datetime import datetime
from django.db.models import Q
from telegram_bot.models import Student, Schedule



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
