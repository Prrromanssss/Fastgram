from delivery.calculation_of_delivery import CalculationDelivery
from delivery.forms import DeliveryForm
from delivery.models import Delivery
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


class DeliveryView(FormView):
    template_name = 'delivery/delivery.html'
    model = Delivery
    form_class = DeliveryForm
    context_object_name = 'form'
    success_url = reverse_lazy('delivery:show')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            calculation_delivery = CalculationDelivery(form.cleaned_data)
            try:
                calculate_l_post = calculation_delivery.calculate_l_post()
            except Exception:
                calculate_l_post = []
            calculate_cse = []
            return render(request, 'delivery/show_deliveries.html',
                          {'args_l_post': calculate_l_post,
                           'args_cse': calculate_cse})
            # return redirect(self.get_success_url())

        if form.is_valid():
            return redirect(self.get_success_url())
        else:
            return render(request, 'delivery/show_deliveries.html',
                          {'args_l_post': [],
                           'args_cse': []})

        # return render(request, self.template_name)


class DeliveryShowView(TemplateView):
    template_name = 'delivery/show_deliveries.html'


class DeliveryTaxiView(TemplateView):
    template_name = 'delivery/taxi_deliveries.html'
