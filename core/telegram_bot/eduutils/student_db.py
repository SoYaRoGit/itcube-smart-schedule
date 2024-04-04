from telegram_bot.models import Student, Schedule


def student_to_dict(student):
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
        student_data = student_to_dict(student)
        return student_data
    except Student.DoesNotExist:
        # Обработка случая, когда студент с указанным telegram_id не найден
        return None