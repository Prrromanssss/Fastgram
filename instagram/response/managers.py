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
                'delivery__name',
                'mainimage__image',
                'user__email',
            )
        )
