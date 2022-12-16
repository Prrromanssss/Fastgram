from django.urls import path
from response import views

app_name = 'response'

urlpatterns = [
    path('', views.ListCommentsView.as_view(), name='list_responses'),
]
