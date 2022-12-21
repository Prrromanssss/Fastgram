from django.urls import path
from response import views

app_name = 'response'

urlpatterns = [
    path('', views.ListResponsesView.as_view(), name='list_responses'),
    path('like/<int:response_id>/', views.LikeResponse.as_view(), name='like'),
]
