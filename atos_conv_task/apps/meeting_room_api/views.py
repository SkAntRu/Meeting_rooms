from rest_framework.permissions import IsAuthenticated
from meeting_room.models import MeetingRoom
from .serializers import MeetingRoomSerializer
from rest_framework import viewsets


class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    """List of all Meeting Rooms"""
    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingRoomSerializer

    def get_queryset(self):
        return MeetingRoom.objects.all()
