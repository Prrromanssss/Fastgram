from django.views.generic import TemplateView


class ListCommentsView(TemplateView):
    template_name = 'comments/list_comments.html'
