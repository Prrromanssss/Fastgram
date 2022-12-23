from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from delivery.delivery_calcultaion import CalculateBoxberry, CalculateLPost
from delivery.forms import DeliveryForm
from delivery.models import Delivery


class DeliveryView(FormView):
    template_name = 'delivery/delivery.html'
    template_name_for_show_deliveries = 'delivery/show_deliveries.html'
    model = Delivery
    form_class = DeliveryForm
    success_url = reverse_lazy('delivery:show')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apikey'] = settings.YANDEX_MAPS_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            form_params = form.cleaned_data
            weight = form_params['weight']
            length = form_params['length']
            width = form_params['width']
            height = form_params['height']
            cost = form_params['cost']
            city_from = form_params['city_from'].capitalize()
            city_to = form_params['city_to'].capitalize()
            try:
                l_post_delivery = CalculateLPost(
                    weight, length, width, height,
                    cost, city_from, city_to
                    )
                calculate_l_post = l_post_delivery.calculate_l_post()
            except KeyError:
                calculate_l_post = []
            try:
                boxberry_delivery = CalculateBoxberry(
                    weight, length, width,
                    height, cost, city_from,
                    city_to
                    )
                calculate_boxberry = boxberry_delivery.calculate_boxberry()
            except KeyError:
                calculate_boxberry = []

            return render(
                request,
                self.template_name_for_show_deliveries,
                {
                    'args_l_post': calculate_l_post,
                    'args_boxberry': calculate_boxberry,
                    }
                )

        return render(
            request,
            self.template_name_for_show_deliveries,
            )


class DeliveryShowView(TemplateView):
    template_name = 'delivery/show_deliveries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apikey'] = settings.YANDEX_MAPS_API_KEY
        return context


class DeliveryTaxiView(TemplateView):
    template_name = 'delivery/taxi_deliveries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apikey'] = settings.YANDEX_MAPS_API_KEY
        return context
