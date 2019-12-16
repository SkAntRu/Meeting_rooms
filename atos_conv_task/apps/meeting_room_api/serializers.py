from rest_framework import serializers
from meeting_room.models import MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = (
            'meeting_room_name',
            'amount_of_chairs',
            'projector',
            'flip_chart',
            'description',
        )
