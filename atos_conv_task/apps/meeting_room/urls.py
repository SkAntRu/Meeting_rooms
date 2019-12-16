from django.urls import path
from . import views


app_name = 'meeting_room'
urlpatterns = [
    path('', views.index, name='index'),
    path('mr_<meeting_room_name>/', views.details, name='Details'),
    path('login_page/', views.mr_login, name='Login'),
    path('logout/', views.mr_logout, name='Logout'),
    path('reserve_room_<str:meeting_room_name>/', views.reserve_room, name='Reserve room'),
    path('reserve_room/', views.reserve_room, name='reserve_room'),
    path('accept_bid_<int:bid_pk>/', views.accept_bid),
    path('decline_bid_<int:bid_pk>/', views.decline_bid),
    path('customize_room_<str:meeting_room_name>/', views.customize_room, name='Customize meeting room'),
    path('manage_users/', views.manage_users, name='Выдать права Офис-менеджера'),
    path('group_add_member_<int:user_id>/', views.group_add_member),
    path('group_delete_member_<int:user_id>/', views.group_delete_member),
]
