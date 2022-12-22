from django.urls import path

from response import views

app_name = 'response'

urlpatterns = [
    path(
        '',
        views.ListResponsesView.as_view(),
        name='list_responses',
        ),
    path(
        'response_detail/<int:pk>/',
        views.ResponseDetailView.as_view(),
        name='response_detail',
        ),
    path(
        'like/<int:response_id>/?page=<int:page_number>/'
        '&is_detail=<str:is_detail>/',
        views.LikeResponseView.as_view(),
        name='like',
        ),
    path(
        'comment/<int:response_id>/?page=<int:page_number>/'
        '&is_detail=<str:is_detail>/',
        views.CommentResponse.as_view(),
        name='comment',
        ),
]
