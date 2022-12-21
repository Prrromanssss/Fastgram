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
        'вес', validators=[MinValueValidator(0.1), MaxValueValidator(1000)])
    length = models.IntegerField(
        'длина', validators=[MinValueValidator(1), MaxValueValidator(120)])
    width = models.IntegerField(
        'ширина', validators=[MinValueValidator(1), MaxValueValidator(80)])
    height = models.IntegerField(
        'высота', validators=[MinValueValidator(1), MaxValueValidator(50)])

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
        default=Subjects.main_city
    )
    # district_from = models.CharField(
    #     'Округ отправки посылки', max_length=50, blank=True, default='',
    #     help_text='Максимум 50 символов')

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
        default=Subjects.main_city
    )
    # district_to = models.CharField(
    #     'Округ получения посылки', max_length=50, blank=True, default='',
    #     help_text='Максимум 50 символов')
