from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ('password',)
    list_display = ('email', 'nickname', 'is_staff', 'is_active',)
    list_filter = ('email', 'nickname', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password', 'first_name',
                'last_name', 'birthday')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nickname',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            )}),
    )
    search_fields = ('nickname', 'email')
    ordering = ('nickname', 'email')
