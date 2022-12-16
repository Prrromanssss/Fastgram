from ckeditor.fields import RichTextField
from core.models import ImageBaseModel, IsPublishedBaseModel, NameBaseModel
from django.db import models
from response.managers import ResponseManager
from users.models import CustomUser


class Response(NameBaseModel):
    objects = ResponseManager()

    delivery = models.ForeignKey(
        'Delivery',
        verbose_name='курьерская служба',
        on_delete=models.CASCADE,
        help_text='Выберите курьерскую служба',
    )
    text = RichTextField(
        'описание',
        help_text='Подробно расскажите о впечатлениях от данной'
        ' курьерской службы',
    )
    created_on = models.DateTimeField(
        'дата написания',
        auto_now_add=True,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='user_response',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Delivery(NameBaseModel, IsPublishedBaseModel):
    weight = models.PositiveSmallIntegerField(
        'вес',
        default=100,
        help_text='Максимум 32767',
    )

    class Meta:
        verbose_name = 'курьерская служба'
        verbose_name_plural = 'курьерские службы'


class MainImage(ImageBaseModel):
    response = models.OneToOneField(
        'Response',
        verbose_name='отзыв',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
