from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram_bot.models import Student, Teacher
from telegram_bot.eduutils.edu_utils_db import get_groups_teacher
from asgiref.sync import sync_to_async



def send_full_name(telegram_id: int) -> str:
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
            return str(teacher.full_name)  # Если аутентифицирован, возвращаем True


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
    student = Student.objects.get(
        login = state_data['login'],
        password = state_data['password']
    )
    
    # Если студент c такими данными существует и он не авторизован, то проводим аутентификацию
    if student and not student.is_authentication == True:
        Student.objects.filter(
            login = state_data['login'],
            password = state_data['password']
        ).update(
            telegram_id = telegram_id,
            is_authentication = True
        )
        
        return True
    
    # Проверяем, существует ли преподаватель с указанным логином, паролем
    teacher = Teacher.objects.get(
        login = state_data['login'],
        password = state_data['password']
    )
    
    # Если преподаватель c такими данными существует, то проводим аутентификацию
    if teacher and not teacher.is_authentication == True:
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
    



def authentication_student(telegram_id: int) -> bool:
    # Проверяем, существует ли студент с указанным telegram_id
    student_exists = Student.objects.filter(telegram_id=telegram_id).exists()
        
    # Если студент существует, проверяем его аутентификацию
    if student_exists:
        student = Student.objects.get(telegram_id=telegram_id)
        if student.is_authentication:
            return True  # Если аутентифицирован, возвращаем False
    
    return False


class AuthenticationStudentFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        telegram_id: int = message.from_user.id
        return await sync_to_async(authentication_student)(telegram_id)
    
    


def authentication_teacher(telegram_id: int) -> bool:
    # Проверяем, существует ли студент с указанным telegram_id
    teacher_exists = Teacher.objects.filter(telegram_id=telegram_id).exists()
        
    # Если студент существует, проверяем его аутентификацию
    if teacher_exists:
        teacher = Teacher.objects.get(telegram_id=telegram_id)
        if teacher.is_authentication:
            return True  # Если аутентифицирован, возвращаем False
    
    return False

class AuthenticationTeacherFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        telegram_id: int = message.from_user.id
        return await sync_to_async(authentication_teacher)(telegram_id)
    
    
class CallbackTeacherGroupsFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        teacher_groups: list[tuple[str]] = await sync_to_async(get_groups_teacher)(callback.from_user.id)
        
        for group_tuple in teacher_groups:
            if callback.data in group_tuple:
                return {'group': group_tuple[0]}  # Возвращаем первый элемент кортежа
        
        return False