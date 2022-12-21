from django.urls import path
from response import views

app_name = 'response'

urlpatterns = [
    path(
        '',
        views.ListResponsesView.as_view(),
        name='list_responses'
        ),
    path(
        'response_detail/<int:pk>',
        views.ResponseDetailView.as_view(),
        name='response_detail'
        ),
    path(
        'like/<int:response_id>/',
        views.LikeResponse.as_view(),
        name='like'
        ),
]
