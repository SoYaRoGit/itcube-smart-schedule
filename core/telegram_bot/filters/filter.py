from aiogram.filters import BaseFilter
from aiogram.types import Message
from telegram_bot.models import Student, Teacher
from asgiref.sync import sync_to_async



class NotAuthenticationFilter(BaseFilter):
    def is_authenticated(telegram_id: int) -> bool:
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
    
    async def __call__(self, message: Message) -> bool:
        telegram_id = message.from_user.id
        return await sync_to_async(self.is_authenticated)(telegram_id)
