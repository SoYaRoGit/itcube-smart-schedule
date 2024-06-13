from django.db import models
from telegram_bot.utils.crypt import CryptoManager

class Student(models.Model):
    """
    Модель для хранения информации о студентах.

    Attributes:
        login (str): Логин студента. Уникальное поле, используется для аутентификации.
        password (str): Пароль студента. Используется для аутентификации.
        full_name (str): Полное имя студента.
        telegram_id (int): Идентификатор Telegram студента, используется для связи.
        is_authentication (bool): Флаг, указывающий на состояние аутентификации студента.
    """

    login = models.CharField(
        verbose_name="Логин",
        max_length=30,
        unique=True,
        blank=False,
        help_text="Укажите логин для ученика",
    )

    password = models.CharField(
        verbose_name="Пароль",
        max_length=30,
        blank=False,
        help_text="Укажите пароль для ученика",
    )

    full_name = models.CharField(
        verbose_name="ФИО",
        max_length=50,
        unique=False,
        blank=False,
        help_text="Укажите ФИО ученика",
    )

    telegram_id = models.PositiveBigIntegerField(
        verbose_name="Телеграм ID",
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text="Указывается телеграм ID после аутентификации",
    )

    is_authentication = models.BooleanField(
        verbose_name="Аутентификация",
        blank=True,
        default=False,
        help_text="Состояние аутентификации",
    )

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        """
        Метод для представления объекта студента в виде строки.
        
        Returns:
            str: Полное имя студента.
        """
        return self.full_name


class StudentGroup(models.Model):
    """
    Модель для хранения информации о группах учеников.

    Attributes:
        name (str): Название группы. Уникальное поле, идентифицирует группу.
        teacher (Teacher): Преподаватель, который ведет занятия с этой группой. 
        students (ManyToManyField): Список учеников, состоящих в данной группе.
    """

    name = models.CharField(
        verbose_name="Название группы",
        max_length=50,
        blank=False,
        unique=True,
        db_index=True,
        help_text="Создайте группу",
    )

    teacher = models.ForeignKey(
        to="Teacher",
        on_delete=models.CASCADE,
        verbose_name="Преподаватель",
        blank=False,
        null=True,
        help_text="Укажите преподавателя, который преподает дисциплину",
    )

    students = models.ManyToManyField(
        to=Student,
        verbose_name="В каких группах состоит ученик",
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        """
        Метод для представления объекта группы в виде строки.
        
        Returns:
            str: Название группы.
        """
        return self.name


class StudentContentDetails(models.Model):
    """
    Модель для хранения дополнительной информации о студентах.

    Attributes:
        parent_full_name (str): ФИО родителя или законного представителя студента.
        parent_residential_adress (str): Место регистрации родителя или законного представителя.
        student (Student): Связь с объектом студента, к которому относятся эти данные.
        date_birth (date): Дата рождения студента.
        if_fourteen (bool): Флаг, указывающий, достиг ли студент 14 лет.
        student_residential_adress (str): Адрес проживания студента с индексом.
        passport_data (str): Паспортные данные студента (номер и серия).
        passport_data_issued_by (str): Организация, выдавшая паспорт студенту.
        passport_data_date_of_issueс (date): Дата выдачи паспорта студенту.
        name_education_organization (str): Название учебной организации, в которой учится студент.
        certificate_number (str): Номер сертификата студента.
        parent_contact (str): Контактные данные родителя или законного представителя (телефон, эл. почта).
        student_contact (str): Контактные данные студента (телефон, эл. почта).
        medical_restrictions (bool): Флаг, указывающий на наличие медицинских ограничений у студента.
        date_contract (date): Дата заключения контракта о предоставлении образовательных услуг.

    """

    parent_full_name = models.CharField(
        verbose_name="ФИО Родителя",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите ФИО Родителя (законного представителя)",
    )

    parent_residential_adress = models.CharField(
        verbose_name="Место регистрации родителя",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите место регистрации родителя (законного представителя)",
    )

    student = models.OneToOneField(
        to=Student,
        on_delete=models.CASCADE,
        verbose_name="Ученик",
        blank=False,
        help_text="Укажите для кого указываются данные",
    )

    date_birth = models.CharField(
        verbose_name="Дата рождения",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите дату рождения"
    )

    if_fourteen = models.BooleanField(
        verbose_name="Достиг ли ученик 14-го возраста",
        default=False,
        help_text="Укажите достиг ли ученик 14-го возраста",
    )

    student_residential_adress = models.CharField(
        verbose_name="Адрес проживания",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите адрес проживания с индексом",
    )

    passport_data = models.CharField(
        verbose_name="Паспортные данные",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите паспортные данные(номер, серия)",
    )

    passport_data_issued_by = models.CharField(
        verbose_name="Кем выдан",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите кем выдан паспорт",
    )

    passport_data_date_of_issueс = models.CharField(
        verbose_name="Дата выдачи",
        max_length=255,
        null=True,
        blank=True,
        help_text="Укажите дату выдачи паспорта"
    )

    name_education_organization = models.CharField(
        verbose_name="Учебная организация",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите название учебной организации",
    )

    certificate_number = models.CharField(
        verbose_name="Номер сертификата",
        max_length=255,
        unique=True,
        blank=False,
        help_text="Укажите номер сертификата",
    )

    parent_contact = models.CharField(
        verbose_name="Контактные данные родителя",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите контактные данные родителя (номер телефона, эл. почта)",
    )

    student_contact = models.CharField(
        verbose_name="Контактные данные ученика",
        max_length=255,
        blank=True,
        null=True,
        help_text="Укажите контактные данные родителя (номер телефона, эл. почта)",
    )

    medical_restrictions = models.BooleanField(
        verbose_name="Медицинские ограничения",
        default=False,
        help_text="Укажите медицинские ограничения (да/нет)",
    )

    date_contract = models.CharField(
        verbose_name="Дата заключения контракта",
        max_length=255,
        blank=False,
        help_text="Укажите дату заключения контракта",
    )

    class Meta:
        verbose_name = "Дополнительная информация о ученике"
        verbose_name_plural = "Дополнительная информация о учениках"

    def __str__(self) -> str:
        """
        Метод для представления объекта дополнительной информации о студенте в виде строки.
        
        Returns:
            str: Полное имя студента, к которому относятся эти данные.
        """
        return self.student.full_name
    
    def save(self, *args, **kwargs):
        crypto_manager = CryptoManager()
        self.parent_full_name: models.CharField = crypto_manager.encrypt(self.parent_full_name)
        self.parent_residential_adress: models.CharField = crypto_manager.encrypt(self.parent_residential_adress)
        self.date_birth: models.CharField = crypto_manager.encrypt(self.date_birth)
        self.student_residential_adress: models.CharField = crypto_manager.encrypt(self.student_residential_adress)
        self.passport_data: models.CharField = crypto_manager.encrypt(self.passport_data)
        self.passport_data_issued_by: models.CharField = crypto_manager.encrypt(self.passport_data_issued_by)
        self.passport_data_date_of_issueс: models.CharField = crypto_manager.encrypt(self.passport_data_issued_by)
        self.name_education_organization: models.CharField = crypto_manager.encrypt(self.name_education_organization)
        self.certificate_number: models.CharField = crypto_manager.encrypt(self.certificate_number)
        self.parent_contact: models.CharField = crypto_manager.encrypt(self.parent_contact)
        self.student_contact: models.CharField = crypto_manager.encrypt(self.student_contact)
        self.date_contract: models.CharField = crypto_manager.encrypt(self.date_contract)
        super().save(*args, **kwargs)


class Teacher(models.Model):
    """
    Модель для хранения информации о преподавателях.

    Attributes:
        login (str): Логин преподавателя. Уникальное поле, используется для аутентификации.
        password (str): Пароль преподавателя. Используется для аутентификации.
        full_name (str): Полное имя преподавателя.
        telegram_id (int): Идентификатор Telegram преподавателя, используется для связи.
        is_authentication (bool): Флаг, указывающий на состояние аутентификации преподавателя.
    """

    login = models.CharField(
        verbose_name="Логин",
        max_length=30,
        unique=True,
        blank=False,
        help_text="Укажите логин для преподавателя",
    )

    password = models.CharField(
        verbose_name="Пароль",
        max_length=30,
        blank=False,
        help_text="Укажите пароль для преподавателя",
    )

    full_name = models.CharField(
        verbose_name="ФИО",
        max_length=50,
        unique=False,
        blank=False,
        help_text="Укажите ФИО преподавателя",
    )

    telegram_id = models.PositiveBigIntegerField(
        verbose_name="Телеграм ID",
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text="Указывается телеграм ID после аутентификации",
    )

    is_authentication = models.BooleanField(
        verbose_name="Аутентификация",
        blank=True,
        default=False,
        help_text="Состояние аутентификации",
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        """
        Метод для представления объекта преподавателя в виде строки.
        
        Returns:
            str: Полное имя преподавателя.
        """
        return self.full_name


class Subject(models.Model):
    """
    Модель для хранения информации о дисциплинах.

    Attributes:
        name (str): Название дисциплины. Уникальное поле, идентифицирует дисциплину.
    """

    name = models.CharField(
        verbose_name="Название дисциплины",
        max_length=50,
        blank=False,
        unique=True,
        db_index=True,
        help_text="Укажите название дисциплины",
    )

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        """
        Метод для представления объекта дисциплины в виде строки.
        
        Returns:
            str: Название дисциплины.
        """
        return self.name


class Classroom(models.Model):
    """
    Модель для хранения информации о кабинетах.

    Attributes:
        name (str): Название кабинета.
    """

    name = models.CharField(
        verbose_name="Название кабинета",
        max_length=50,
        blank=False,
        help_text="Укажите название кабинета",
    )

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"

    def __str__(self):
        """
        Метод для представления объекта кабинета в виде строки.
        
        Returns:
            str: Название кабинета.
        """
        return self.name


class Schedule(models.Model):
    """
    Модель для хранения расписания занятий.

    Attributes:
        date (date): Дата занятия.
        start_time (time): Время начала занятия.
        end_time (time): Время окончания занятия.
        subject (Subject): Дисциплина, которая преподается на занятии.
        classroom (Classroom): Кабинет, в котором проходит занятие.
        group (StudentGroup): Группа, для которой назначено занятие.
    """

    date = models.DateField(
        verbose_name="Дата занятия", 
        blank=False, 
        help_text="Укажите дату занятия"
    )

    start_time = models.TimeField(
        verbose_name="Время начала занятия",
        blank=False,
        help_text="Укажите время начала занятия",
    )

    end_time = models.TimeField(
        verbose_name="Время окончания занятия",
        blank=False,
        help_text="Укажите время окончания занятия",
    )

    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        verbose_name="Дисциплина",
        blank=False,
        help_text="Укажите дисциплину",
    )

    classroom = models.ForeignKey(
        to=Classroom,
        on_delete=models.CASCADE,
        verbose_name="Кабинет",
        blank=False,
        help_text="Укажите кабинет",
    )

    group = models.ForeignKey(
        to=StudentGroup,
        on_delete=models.CASCADE,
        verbose_name="Группа",
        blank=False,
        help_text="Укажите группу",
    )

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        """
        Метод для представления объекта занятия в виде строки.
        
        Returns:
            str: Строка, представляющая занятие в формате "Дисциплина Кабинет Дата Время начала - Время окончания".
        """
        return f"{self.subject.name} {self.classroom.name} {self.date} {self.start_time} - {self.end_time}"
