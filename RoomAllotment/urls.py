from django.urls import path

from . import views

#urlpatterns = [
#    path('request/<int:request_id>/', views.request_detail, name='detail'),
#    path('request/create/', views.request_form, name='form'),
#    path('requests/', views.view_requests, name='view request'),
#]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('student/<int:std_id>', views.StudentHomeView.as_view(), name='student-home'),
    path('provost/<int:prv_id>', views.ProvostHomeView.as_view(), name='provost-home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('student/<int:std_id>/room-req', views.StudentRoomReqView.as_view(), name='student-room-req'),
    path('provost/<int:prv_id>/room-allot', views.ProvostRoomAllotView.as_view(), name='provost-room-allot'),
]
