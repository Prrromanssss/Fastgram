from django import forms
<<<<<<< HEAD:fastgram/response/forms.py
from response.models import MainImage, Response


class MainImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = MainImage
        fields = (
            MainImage.image.field.name,
        )
=======
from response.models import Response, Comment
>>>>>>> 6aed3a901438afc0b634a3569a406f99fa535e0b:instagram/response/forms.py


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
            Response.grade.field.name,
        )
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
            }),
        }


class CommentForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = (
            Comment.text.field.name,
        )
        widgets = {
            Comment.text.field.name: forms.Textarea()
        }
