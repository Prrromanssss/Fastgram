from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from response.forms import ResponseForm
from response.models import Response


class ListCommentsView(ListView, FormView):
    model = Response
    form_class = ResponseForm
    template_name = 'response/list_responses.html'
    context_object_name = 'responses'
    get_queryset = Response.objects.list_responses
    success_url = reverse_lazy('response:list_responses')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
