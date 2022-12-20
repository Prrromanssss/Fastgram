from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from response.forms import MainImageForm, ResponseForm
from response.models import MainImage, Response


class ListResponsesView(ListView, FormView):
    model = Response
    model_image = MainImage
    form_class = ResponseForm
    form_image_class = MainImageForm
    template_name = 'response/list_responses.html'
    get_queryset = Response.objects.list_responses
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.form_image_class(
            self.request.POST or None,
            self.request.FILES,
        )
        return context

    def get_success_url(self):
        success_url = reverse_lazy('response:list_responses')
        if 'page' in self.request.GET:
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            success_url += f'?page={context["paginator"].num_pages}'
        return success_url

    def form_valid(self, form):
        image_form = self.form_image_class(
            self.request.POST or None,
            self.request.FILES,
        )
        if self.request.user and image_form.is_valid():
            response = self.model.objects.create(
                        user=self.request.user,
                        **form.cleaned_data,
                    )
            self.model_image.objects.create(
                response=response,
                **image_form.cleaned_data,
            )
        return super().form_valid(form)


class LikeResponse(FormView):
    model = Response
    success_url = reverse_lazy('response:list_responses')

    def post(self, request, response_id):
        response = self.model.objects.filter(
            id=response_id,
        )
        like = response.filter(likes=request.user).first()

        if like:
            like.likes.remove(request.user)
        else:
            response.first().likes.add(request.user)
            response.first().save()

        return redirect(self.get_success_url())
