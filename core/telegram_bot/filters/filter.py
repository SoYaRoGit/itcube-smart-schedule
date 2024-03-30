from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram_bot.models import Student, Teacher
from asgiref.sync import sync_to_async



def not_authentication(telegram_id: int) -> bool:
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

class NotAuthenticationFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        telegram_id = message.from_user.id
        return await sync_to_async(not_authentication)(telegram_id)


def authentication_update(telegram_id: int, state_data) -> bool:
    # Проверяем, существует ли студент с указанным логином, паролем
    student = Student.objects.filter(
        login = state_data['login'],
        password = state_data['password']
    ).exists()
    
    # Если студент c такими данными существует, то проводим аутентификацию
    if student:
        Student.objects.filter(
            login = state_data['login'],
            password = state_data['password']
        ).update(
            telegram_id = telegram_id,
            is_authentication = True
        )
        
        return True
    
    # Проверяем, существует ли преподаватель с указанным логином, паролем
    teacher = Teacher.objects.filter(
        login = state_data['login'],
        password = state_data['password']
    ).exists()
    
    # Если преподаватель c такими данными существует, то проводим аутентификацию
    if teacher:
        Teacher.objects.filter(
            login = state_data['login'],
            password = state_data['password']
        ).update(
            telegram_id = telegram_id,
            is_authentication = True
        )
        
        return True
    
    # В случае, если не найдены данные, то возвращаем False
    return False

class AuthenticationUpdateFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, state: FSMContext):
        telegram_id = callback.from_user.id
        state_data = await state.get_data()
        return await sync_to_async(authentication_update)(telegram_id, state_data)