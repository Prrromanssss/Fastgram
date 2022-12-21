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

    likes = models.ManyToManyField(
        CustomUser,
        verbose_name='лайк',
        blank=True,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def get_likes(self):
        return self.likes.only('id')

    def get_comments(self):
        return Comment.objects.filter(
            response=self
        ).all()


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


class Comment(models.Model):
    text = RichTextField(
        'текст',
        help_text='Напишите свой комментарий'
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    response = models.ForeignKey(
        Response,
        verbose_name='отзыв',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.user} к \'{self.response}\''
