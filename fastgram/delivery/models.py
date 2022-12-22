from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Delivery(models.Model):
    class Subjects(models.TextChoices):
        main_city = '1', 'город федерального значения'
        republic = '2', 'республика'
        edge = '3', 'край'
        area = '4', 'область'
        AA = '5', 'автономный округ'
        AO = '6', 'автономная область'

    weight = models.FloatField(
        'вес', validators=[MinValueValidator(0.1), MaxValueValidator(30)],
        help_text='Введите вес посылки от 0.1 до 1400 кг',
        default=0.1)
    length = models.IntegerField(
        'длина', validators=[MinValueValidator(1), MaxValueValidator(120)],
        help_text='Введите высоту посылки от 1 до 120 см')
    width = models.IntegerField(
        'ширина', validators=[MinValueValidator(1), MaxValueValidator(80)],
        help_text='Введите высоту посылки от 1 до 80 см')
    height = models.IntegerField(
        'высота', validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text='Введите высоту посылки от 1 до 50 см')
    cost = models.IntegerField(
        'стоимость посылки', validators=[MinValueValidator(500),
                                         MaxValueValidator(200000)],
        help_text='Введите стоимость посылки от 500 до 200000 рублей',
        default=1000)

    city_from = models.CharField(
        'Город отправки посылки', max_length=50,
        help_text='Максимум 50 символов')
    subject_from = models.CharField(
        'Субъект РФ отправки посылки', max_length=50,
        help_text='Введите только название субъекта, максимум 50 символов')
    subject_type_from = models.CharField(
        'Тип субъекта',
        max_length=2,
        choices=Subjects.choices,
        default=Subjects.main_city,
        help_text='Выберите тип субъекта из выпадающего списка'
    )

    city_to = models.CharField(
        'Город получения посылки', max_length=50,
        help_text='Максимум 50 символов')
    subject_to = models.CharField(
        'Субъект РФ получения посылки', max_length=50,
        help_text='Введите только название субъекта, максимум 50 символов')
    subject_type_to = models.CharField(
        'Тип субъекта',
        max_length=2,
        choices=Subjects.choices,
        default=Subjects.main_city,
        help_text='Выберите тип субъекта из выпадающего списка'
    )
