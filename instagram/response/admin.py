from django.contrib import admin
from response.models import Delivery, MainImage, Response, Comment


class MainImageInline(admin.TabularInline):
    model = MainImage
    readonly_fields = ('image_tmb',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    fields = ('name', 'is_published', 'weight')
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        'small_image_tmb',
        'name',
        'delivery_name',
    )
    list_display_links = ('name',)
    inlines = [
        MainImageInline,
    ]

    def delivery_name(self, obj):
        return obj.delivery.name
    delivery_name.short_description = 'курьерская служба'

    def small_image_tmb(self, obj):
        if obj.mainimage:
            return obj.mainimage.small_image_tmb()
        return 'Нет изображения'
    small_image_tmb.short_description = 'главное изображение'


@admin.register(MainImage)
class MainImageAdmin(admin.ModelAdmin):
    list_display = ('small_image_tmb', 'response_name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'response',
    )
