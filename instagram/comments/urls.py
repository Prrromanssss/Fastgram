from comments import views
from django.urls import path

app_name = 'comments'

urlpatterns = [
    path('', views.ListCommentsView.as_view(), name='list_comments'),
]
