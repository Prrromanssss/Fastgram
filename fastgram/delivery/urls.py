from delivery import views
from django.urls import path

app_name = 'delivery'

urlpatterns = [
    path('', views.DeliveryView.as_view(), name='delivery'),
    path('shows', views.DeliveryShowView.as_view(), name='show'),
    path('taxi', views.DeliveryTaxiView.as_view(), name='taxi'),
]
