from django.db import models


class ResponseManager(models.Manager):
    def list_responses(self):
        return (
            self.get_queryset()
            .select_related('delivery', 'mainimage', 'user')
            .filter(
                delivery__is_published=True
            )
            .only(
                'name',
                'text',
                'created_on',
                'delivery__name',
                'delivery__another_link',
                'mainimage__image',
                'user__email',
            )
        )
