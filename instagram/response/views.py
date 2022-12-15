from django.views.generic import FormView, ListView
from response.forms import ResponseForm
from response.models import Response


class ListCommentsView(ListView, FormView):
    model = Response
    form_class = ResponseForm
    template_name = 'response/list_responses.html'
