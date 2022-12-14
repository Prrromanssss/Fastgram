from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    password = None

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birthday')
