from django import forms
from response.models import Response


class ResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Response
        fields = (
            Response.name.field.name,
            Response.delivery.field.name,
            Response.text.field.name,
        )
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
            })
        }
