from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from response.forms import ResponseForm
from response.models import Response


class ListResponsesView(ListView, FormView):
    model = Response
    form_class = ResponseForm
    template_name = 'response/list_responses.html'
    context_object_name = 'responses'
    get_queryset = Response.objects.list_responses
    paginate_by = 5

    def get_success_url(self):
        success_url = reverse_lazy('response:list_responses')
        if 'page' in self.request.GET:
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            success_url += f'?page={context["paginator"].num_pages}'
        return success_url

    def form_valid(self, form):
        if self.request.user:
            self.model.objects.create(
                user=self.request.user,
                **form.cleaned_data,
            )
        return super().form_valid(form)
