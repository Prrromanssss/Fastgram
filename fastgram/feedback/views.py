from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FeedbackView(FormView):
    template_name = 'feedback/feedback.html'
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback:feedback')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        text = form.cleaned_data['text']
        mail = form.cleaned_data['mail']
        message = (
            f'Здравствуйте, {name}! '
            'Вы получили это письмо, так как написали в Boyko Company.\n'
            f'Ваш отзыв:\n{text}\n\n'
            'Спасибо за фидбэк! Мы обязательно учтем ваше мнение.\n'
            '© Boyko Company'
        )
        send_mail(
            'Boyko company',
            message,
            settings.ADMIN_EMAIL,
            [mail],
            fail_silently=False,
        )
        self.model.objects.create(
            **form.cleaned_data
        )
        return super().form_valid(form)
