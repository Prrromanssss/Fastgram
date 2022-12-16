from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.shortcuts import render, redirect

from users.forms import CustomUserCreationForm, CustomUserChangeForm
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


class ProfileView(TemplateView):
    template_name = 'users/profile.html'


# Не особо понял что к чему тут должно быть в этих ваших классах
class ProfileChangeView(FormView):
    template_name = 'users/profile_change.html'
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:profile')

    def get(self, request):
        form = self.form_class(
            initial=self.initial,
            instance=request.user,
        )
        context = {'form': form, 'user': request.user}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(
            request.POST or None,
            instance=request.user,
        )
        if form.is_valid():
            self.model.objects.filter(id=request.user.id).update(
                **form.cleaned_data,
            )
            return redirect(self.get_success_url())
        context = {'form': form, 'user': request.user}
        return render(request, self.template_name, context)
