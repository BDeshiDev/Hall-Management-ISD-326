from django.urls import path

from . import views
from . import common_views
from . import student_views
from . import provost_views

#urlpatterns = [
#    path('request/<int:request_id>/', views.request_detail, name='detail'),
#    path('request/create/', views.request_form, name='form'),
#    path('requests/', views.view_requests, name='view request'),
#]

urlpatterns = [
    path('', common_views.HomeView.as_view(), name='home'),
    path('student/<int:std_id>', student_views.StudentHomeView.as_view(), name='student-home'),
    path('provost/<int:prv_id>', provost_views.ProvostHomeView.as_view(), name='provost-home'),
    path('login/', common_views.LoginView.as_view(), name='login'),
    path('logout/', common_views.LogoutView.as_view(), name='logout'),
    path('student/<int:std_id>/room-req', student_views.StudentRoomReqView.as_view(), name='student-room-req'),
    path('provost/<int:prv_id>/room-allot', provost_views.ProvostRoomAllotView.as_view(), name='provost-room-allot'),
    path('room-app/<int:app_id>', provost_views.RoomApplicationBasicView.as_view(), name='provost-room-app-see'),
    path('notification_seen_by/<int:id>/<int:notifid>', student_views.NotificationView.as_view(), name='notification'),
]
