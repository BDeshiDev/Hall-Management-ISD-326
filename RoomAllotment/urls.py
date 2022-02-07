from django.urls import path

from . import views

urlpatterns = [
    path('request/<int:request_id>/', views.request_detail, name='detail'),
    path('requests/', views.view_requests, name='view request'),
]