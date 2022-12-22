from django.db import models
from django.db.models import Prefetch
from users.models import CustomUser


class ResponseManager(models.Manager):
    def list_responses(self):
        return (
            self.get_queryset()
            .select_related('delivery', 'mainimage', 'user')
            .prefetch_related(
                Prefetch(
                    'likes', queryset=CustomUser.objects.all(),
                    to_attr='response_likes',
                )
            )
            .only(
                'name',
                'text',
                'grade',
                'created_on',
                'delivery__name',
                'delivery__another_link',
                'mainimage__image',
                'user__email',
                'user__image',
            )
        )
