from django.views.generic import TemplateView


class DeliveryView(TemplateView):
    template_name = 'delivery/route_panel_control.html'
