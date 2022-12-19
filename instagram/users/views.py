from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views.generic import FormView
from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser


class SignUpView(FormView):
    template_name = 'users/sign_up.html'
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:profile')

    def post(self, request):
        form = self.form_class(
            request.POST or None,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            file = form.cleaned_data['image']
            if file:
                FileSystemStorage().save(file.name, file)
            self.model.objects.filter(id=request.user.id).update(
                **form.cleaned_data,
            )

        return super().post(self, request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        return context
