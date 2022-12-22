from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from response.forms import MainImageForm, ResponseForm
from response.models import MainImage, Response


class ListResponsesView(ListView, FormView):
    model = Response
    model_image = MainImage
    form_class = ResponseForm
    form_image_class = MainImageForm
    template_name = 'response/list_responses.html'
    paginate_by = 5
    success_url = reverse_lazy('response:list_responses')

    def get_queryset(self):
        queryset = Response.objects.list_responses()
        searched = self.request.GET.get('searched', '')
        if searched:
            queryset = (
                queryset.
                filter(
                    Q(name__contains=searched)
                    | Q(delivery__name__contains=searched)
                    | Q(text__contains=searched)
                    )
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.form_image_class(
            self.request.POST or None,
            self.request.FILES,
        )
        return context

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


class LikeResponseView(FormView):
    def get_queryset(self):
        return Response.objects.list_responses()

    def post(self, request, response_id, page_number, is_detail):
        is_detail = True if is_detail == 'True' else False

        if is_detail:
            success_url = reverse_lazy(
                'response:response_detail',
                kwargs={'pk': response_id}
                )
        elif page_number:
            success_url = (
                reverse_lazy('response:list_responses')
                + f'?page={page_number}'
                )
        response = self.get_queryset().filter(
            id=response_id,
        )
        like = response.filter(likes=request.user).first()
        if like:
            like.likes.remove(request.user)
        else:
            response.first().likes.add(request.user)
            response.first().save()
        return redirect(success_url)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'response/response_detail.html'

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            return reverse_lazy(
                'response:response_detail',
                kwargs={'pk': kwargs['pk']}
            )
        return reverse_lazy('response:response_detail')

    def get_queryset(self):
        return Response.objects.list_responses()
