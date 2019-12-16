from .views import MeetingRoomViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'meeting_room_all', MeetingRoomViewSet, 'MeetingRoom')

app_name = 'meeting_room_api'
urlpatterns = [
    path('', include(router.urls)),
]
