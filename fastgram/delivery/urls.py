from delivery import views

from django.urls import path

app_name = 'delivery'

urlpatterns = [
    path('', views.DeliveryView.as_view(), name='delivery'),
]
