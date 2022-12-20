from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.shortcuts import redirect
from response.forms import ResponseForm
from response.models import Response


class ListResponsesView(ListView, FormView):
    model = Response
    form_class = ResponseForm
    template_name = 'response/list_responses.html'
    context_object_name = 'responses'
    get_queryset = Response.objects.list_responses
    success_url = reverse_lazy('response:list_responses')

    def post(self, request):
        form = self.get_form()
        if form.is_valid() and request.user:
            self.model.objects.create(
                user=request.user,
                **form.cleaned_data,
            )

        return super().post(self, request)


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
