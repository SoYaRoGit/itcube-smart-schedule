from django.db import models


class Student(models.Model):
    "Ученики"    
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 30,
        unique = True,
        blank = False,
        help_text = 'Укажите логин для ученика'
    )
    
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 30,
        blank = False,
        help_text = 'Укажите пароль для ученика'
    )
    
    full_name = models.CharField(
        verbose_name = 'ФИО',
        max_length = 50,
        unique = False,
        blank = False,
        help_text = 'Укажите ФИО ученика'
    )
    
    telegram_id = models.PositiveBigIntegerField(
        verbose_name = 'Телеграм ID', 
        blank = True, 
        null = True, 
        unique = True, 
        db_index = True, 
        help_text = 'Указывается телеграм ID после аутентификации'
    )
    
    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return self.full_name


class StudentGroup(models.Model):
    """Группа учеников"""
    name = models.CharField(
        verbose_name = 'Название группы',
        max_length = 50,
        blank = False,
        unique = True,
        db_index = True,
        help_text = 'Создайте группу'
    )
    
    teacher = models.ForeignKey(
        to = 'Teacher',
        on_delete = models.CASCADE,
        verbose_name = 'Преподаватель',
        blank = False,
        null = True,
        help_text = 'Укажите преподавателя, который преподает дисциплину'
    )
    
    students = models.ManyToManyField(
        to = Student,
        verbose_name = 'В каких группах состоит ученик',
    )
    
    
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class StudentContentDetails(models.Model):
    """Персональные данные ученика"""
    parent_full_name = models.CharField(
        verbose_name = 'ФИО Родителя',
        max_length = 50,
        blank = True,
        null = True,
        help_text = 'Укажите ФИО Родителя (законного представителя)'
    )
    
    parent_residential_adress = models.CharField(
        verbose_name = 'Место регистрации родителя',
        max_length = 255,
        blank = True,
        help_text = 'Укажите место регистрации родителя (законного представителя)',
    )

    student = models.OneToOneField(
        to = Student,
        on_delete = models.CASCADE,
        verbose_name = 'Ученик',
        blank = False,
        help_text = 'Укажите для кого указываются данные'
    )
    
    date_birth = models.DateField(
        verbose_name = 'Дата рождения',
        blank = True,
        help_text = "Укажите дату рождения"
    )
    
    if_fourteen = models.BooleanField(
        verbose_name = 'Достиг ли ученик 14-го возраста',
        default = False,
        help_text = 'Укажите достиг ли ученик 14-го возраста'
    )
    
    student_residential_adress = models.CharField(
        verbose_name = 'Адрес проживания',
        max_length = 255,
        blank = True,
        help_text = 'Укажите адрес проживания с индексом',
    )
    
    passport_data = models.CharField(
        verbose_name = 'Паспортные данные',
        max_length = 255,
        blank = True,
        help_text = 'Укажите паспортные данные(номер, серия)'
    )
    
    passport_data_issued_by = models.CharField(
        verbose_name = 'Кем выдан',
        max_length = 255,
        blank = True,
        help_text = 'Укажите кем выдан паспорт'
    )
    
    passport_data_date_of_issueс = models.DateField(
        verbose_name = 'Дата выдачи',
        blank = True,
        help_text = 'Укажите дату выдачи паспорта'
    )
    
    name_education_organization = models.CharField(
        verbose_name = 'Учебная организация',
        max_length = 255,
        blank = True,
        help_text = 'Укажите название учебной организации'
    )
    
    certificate_number = models.CharField(
        verbose_name = 'Номер сертификата',
        max_length = 10,
        unique = True,
        blank = False,
        help_text = 'Укажите номер сертификата'
    )
    
    parent_contact = models.CharField(
        verbose_name = 'Контактные данные родителя',
        max_length = 255,
        blank = True,
        help_text = 'Укажите контактные данные родителя (номер телефона, эл. почта)'
    )
    
    student_contact = models.CharField(
        verbose_name = 'Контактные данные ученика',
        max_length = 255,
        blank = True,
        help_text = 'Укажите контактные данные родителя (номер телефона, эл. почта)'
    )
    
    medical_restrictions = models.BooleanField(
        verbose_name = 'Медицинские ограничения',
        default = False,
        help_text = 'Укажите медицинские ограничения (да/нет)'
    )
    
    date_contract = models.DateField(
        verbose_name = 'Дата заключения контракта',
        blank = False,
        help_text = 'Укажите дату заключения контракта'
    )    
    
    class Meta:
        verbose_name = "Дополнительная информация о ученике"
        verbose_name_plural = "Дополнительная информация о учениках"
        
    
    def __str__(self) -> str:
        return self.student.full_name


class Teacher(models.Model):
    """Преподаватели"""
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 30,
        unique = True,
        blank = False,
        help_text = 'Укажите логин для преподавателя'
    )
    
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 30,
        blank = False,
        help_text = 'Укажите пароль для преподавателя'
    )
    
    full_name = models.CharField(
        verbose_name = 'ФИО',
        max_length = 50,
        unique = False,
        blank = False,
        help_text = 'Укажите ФИО преподавателя'
    )
    
    telegram_id = models.PositiveBigIntegerField(
        verbose_name = 'Телеграм ID', 
        blank = True, 
        null = True, 
        unique = True, 
        db_index = True, 
        help_text = 'Указывается телеграм ID после аутентификации'
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.full_name
    

class Subject(models.Model):
    name = models.CharField(
        verbose_name = 'Название дисциплины',
        max_length = 50,
        blank = False,
        unique = True,
        db_index = True,
        help_text = 'Укажите название дисцпиплины'
    )


    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(
        verbose_name = 'Название кабинета',
        max_length = 50,
        blank = False,
        help_text = 'Укажите название кабинета'
    )

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"

    def __str__(self):
        return self.name


class Schedule(models.Model):    
    date = models.DateField(
        verbose_name = 'Дата занятия',
        blank = False,
        help_text = 'Укажите дату занятия'
    )
    
    start_time = models.TimeField(
        verbose_name = 'Время начала занятия',
        blank = False,
        help_text = 'Укажите время начала занятия'
    )
    
    end_time = models.TimeField(
        verbose_name = 'Время окончания занятия',
        blank = False,
        help_text = 'Укажите время окончания занятия'
    )
    
    subject = models.ForeignKey(
        to = Subject,
        on_delete = models.CASCADE,
        verbose_name = 'Дисциплина',
        blank = False,
        help_text = 'Укажите дисциплину'
    )
    
    classroom = models.ForeignKey(
        to = Classroom,
        on_delete = models.CASCADE,
        verbose_name = 'Кабинет',
        blank = False,
        help_text = 'Укажите кабинет'
    )
    
    group = models.ForeignKey(
        to = StudentGroup,
        on_delete = models.CASCADE,
        verbose_name = 'Группа',
        blank = False,
        help_text = 'Укажите группу'
    )

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        return f'{self.subject.name} {self.classroom.name} {self.start_time} - {self.end_time}'