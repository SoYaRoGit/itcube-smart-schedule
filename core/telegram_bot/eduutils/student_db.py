from telegram_bot.models import Student, Schedule
from django.db.models import Prefetch
from asgiref.sync import sync_to_async



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
    schedules = Schedule.objects.filter(group__students=student).all()
    
    schedule_strings = [str(schedule) for schedule in schedules]
    
    return schedule_strings
