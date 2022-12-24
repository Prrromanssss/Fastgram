from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import FormMixin
from response.forms import CommentForm, MainImageForm, ResponseForm
from response.models import Comment, MainImage, Response


class ListResponsesView(FormMixin, ListView):
    model = Response
    model_image = MainImage
    model_comment = Comment
    form_class = ResponseForm
    form_image_class = MainImageForm
    comment_form_class = CommentForm
    template_name = 'response/list_responses.html'
    paginate_by = 5
    success_url = reverse_lazy('response:list_responses')

    def get_queryset(self):
        queryset = Response.objects.list_responses()
        searched = self.request.GET.get('searched', '').lower()
        print(searched)
        if searched:
            queryset = (
                queryset.
                filter(
                    Q(name__icontains=searched)
                    | Q(delivery__name__icontains=searched)
                    | Q(text__icontains=searched)
                    )
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form_class
        context['comments'] = self.model_comment.objects.all_comments()
        context['image_form'] = self.form_image_class(
            self.request.POST or None,
            self.request.FILES,
            )
        return context

    def post(self, request):
        image_form = self.form_image_class(
            self.request.POST or None,
            self.request.FILES,
            )
        form = self.form_class(
            self.request.POST or None
            )
        if self.request.user and image_form.is_valid() and form.is_valid():
            response = self.model.objects.create(
                user=self.request.user,
                **form.cleaned_data,
            )
            self.model_image.objects.create(
                response=response,
                **image_form.cleaned_data,
            )
            return redirect(self.get_success_url())

        return render(request, self.get_success_url(), self.get_context_data())


class LikeResponseView(FormView):
    def get_queryset(self):
        return Response.objects.list_responses()

    def post(self, request, response_id, page_number, is_detail):
        is_detail = is_detail == 'True'
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

        response = get_object_or_404(
            self.get_queryset(),
            id=response_id,
            )

        if request.user in response.likes.all():
            response.likes.remove(request.user)
        else:
            response.likes.add(request.user)
            response.save()
        return redirect(success_url)


class ResponseDetailView(DetailView):
    model_comment = Comment
    comment_form_class = CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form_class
        context['comments'] = self.model_comment.objects.all_comments()
        return context


class CommentResponse(FormView):
    model = Comment

    def post(self, request, response_id, page_number, is_detail):
        is_detail = is_detail == 'True'
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
        form = CommentForm(request.POST or None)
        if form.is_valid():
            self.model.objects.create(
                user=request.user,
                response=Response.objects.get(id=response_id),
                **form.cleaned_data,
            )
        return redirect(success_url)
