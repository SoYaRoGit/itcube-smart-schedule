from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from telegram_bot.models import Student, Schedule, Teacher, StudentGroup, StudentContentDetails
from datetime import timedelta


def __student_to_dict_personal_data(student):
    return {
        'id': student.id,
        'login': student.login,
        'password': student.password,
        'full_name': student.full_name,
        'telegram_id': student.telegram_id,
        'is_authentication': student.is_authentication,
    }

def get_student_send_personal_data(telegram_id: int) -> dict:
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
    return {
        'parent_full_name': student.parent_full_name,
        'parent_residential_adress': student.parent_residential_adress,
        'date_birth': student.date_birth,
        'if_fourteen': student.if_fourteen,
        'student_residential_adress': student.student_residential_adress,
        'passport_data': student.passport_data,
        'passport_data_issued_by': student.passport_data_issued_by,
        'passport_data_date_of_issueс': student.passport_data_date_of_issueс,
        'name_education_organization': student.name_education_organization,
        'certificate_number': student.certificate_number,
        'parent_contact': student.parent_contact,
        'student_contact': student.student_contact,
        'medical_restrictions': student.medical_restrictions,
        'date_contract': student.date_contract
    }

def get_student_confidential_data(telegram_id: int) -> dict:
    try:
        student = StudentContentDetails.objects.get(student__telegram_id = telegram_id)
        student_data = __student_duct_confidential_data(student)
        return student_data
    except Student.DoesNotExist:
        return None

def get_student_send_schedule(telegram_id: int):
    student = Student.objects.get(telegram_id=telegram_id)
    now = datetime.now()  # Получаем текущую дату и время
    
    # Фильтруем расписание по студенту и дате занятия, а также времени начала занятия
    schedules = Schedule.objects.filter(
        Q(date=now.date(), end_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
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
        Q(date=now.date(), end_time__gte=now.time()) | Q(date__gt=now.date()), # Начинающиеся после текущего времени
        group__teacher=teacher,
        date__gte=now.date(),  # Занятия начиная с сегодняшнего дня
    ).order_by('date', 'start_time').all()
    
    schedule_strings = [str(schedule) for schedule in schedules]
    
    return schedule_strings


def student_send_schedule_reminder():
    time_now = datetime.now().replace(second=0, microsecond=0)  # Получаем текущую дату и время
    notification_time_before = timedelta(minutes=2) # Время оповещения до начала занятия
    
    students = Student.objects.all()
    
    students_schedule = {}
    
    for student in students:
        schedules = Schedule.objects.filter(
            date=time_now.date(),  # Занятия только на сегодняшний день
            group__students=student,
            end_time__gte=time_now.time()  # Занятия до момента их окончания
        ).order_by('date', 'start_time').all()
        
        schedule_strings = []
        
        for schedule in schedules:
            start_datetime = timezone.datetime.combine(schedule.date, schedule.start_time)
            end_datetime = timezone.datetime.combine(schedule.date, schedule.end_time)
            
            if time_now == start_datetime - notification_time_before:
                schedule_strings.append(f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")

            if time_now == start_datetime:
                schedule_strings.append(f"[Начало занятия]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")
            
            if time_now == end_datetime:
                schedule_strings.append(f"[Оповещение о завершении]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")
                schedule.delete()
        students_schedule[student.telegram_id] = schedule_strings
    
    return students_schedule


def teacher_send_schedule_reminder():
    tine_now = datetime.now().replace(second=0, microsecond=0)  # Получаем текущую дату и время
    notification_time_before = timedelta(minutes=2) # Время оповещения до начала занятия
    
    teachers = Teacher.objects.all()
    
    teachers_schedule = {}
    
    for teacher in teachers:
        schedules = Schedule.objects.filter(
            date=tine_now.date(),  # Занятия только на сегодняшний день
            group__teacher=teacher,
            end_time__gte=tine_now.time()  # Занятия до момента их окончания
        ).order_by('date', 'start_time').all()
        
        schedule_strings = []
        
        for schedule in schedules:
            start_datetime = timezone.datetime.combine(schedule.date, schedule.start_time)
            end_datetime = timezone.datetime.combine(schedule.date, schedule.end_time)
            
            if tine_now == start_datetime - notification_time_before:
                schedule_strings.append(f"[Оповещение]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")

            if tine_now == start_datetime:
                schedule_strings.append(f"[Начало занятия]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")
            
            if tine_now == end_datetime:
                schedule_strings.append(f"[Оповещение о завершении]\nДата занятия: {schedule.date} | {schedule.start_time} - {schedule.end_time}\nДисциплина: {schedule.subject}\nКабинет: {schedule.classroom}")
                schedule.delete()
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
    
    
def get_students_group_telegram_id(name_group: str) -> list:
    try:
        students_telegram_id = []
        students = Student.objects.filter(studentgroup__name = name_group)
        
        for student in students:
            if student.is_authentication == True:
                students_telegram_id.append(student.telegram_id)
        
        return students_telegram_id
    except Student.DoesNotExist:
        return None
    
def get_students_group_full_name(name_group: str) -> list[str]:
    try:
        students_name = []
        students = Student.objects.filter(studentgroup__name = name_group)
        
        for student in students:
            if student.is_authentication == True:
                students_name.append(student.full_name)
        
        return students_name
    except Student.DoesNotExist:
        return None


def get_groups_teacher(telegram_id_teacher: int) -> list[tuple]:
    groups = StudentGroup.objects.filter(teacher__telegram_id=telegram_id_teacher)
    teacher_groups = [(group.name, str(group)) for group in groups]
    return teacher_groups