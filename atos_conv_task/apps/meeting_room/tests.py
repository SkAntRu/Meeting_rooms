from django.test import TestCase
from meeting_room.models import MeetingRoom, Bid
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class MeetingRoomTestCase(TestCase):
    def setUp(self) -> None:
        new_user = User.objects.create_user('test_user', password='test_user', email='test_user@testuser.com')
        new_user.save()
        new_room = MeetingRoom(meeting_room_name=0)
        new_room.save()
        first_bid = Bid(meeting_room_id=MeetingRoom.objects.get(meeting_room_name=0), time_start=timezone.now(),
                        time_end=timezone.now() + timedelta(hours=1), author=User.objects.get(username='test_user'),
                        )
        first_bid.id = 0
        first_bid.save()
        second_bid = Bid(meeting_room_id=MeetingRoom.objects.get(meeting_room_name=0),
                         time_start=timezone.now() + timedelta(hours=1),
                         time_end=timezone.now() + timedelta(hours=2), author=User.objects.get(username='test_user'),
                         )
        second_bid.id = 1
        second_bid.save()

    def tearDown(self) -> None:
        MeetingRoom.objects.get(meeting_room_name='0').delete()
        User.objects.get(username='test_user').delete()

    def test_meeting_room_all_bids(self):
        cur_room = MeetingRoom(meeting_room_name=0)
        result = cur_room.first_bid()
        self.assertEqual(result, Bid.objects.get(id=0))
        self.assertEqual(1, 0)

    def test_meeting_room_all_bids(self):
        import pytz
        from django.conf import settings
        cur_utc = pytz.timezone(settings.TIME_ZONE)

        cur_room = MeetingRoom(meeting_room_name=0)
        result = cur_room.all_bids()
        assertion = (Bid.objects.filter(meeting_room=self,
                                        time_end__range=(datetime.utcnow().replace(tzinfo=cur_utc),
                                                         (datetime.utcnow().replace(tzinfo=cur_utc)+timedelta(weeks=1)
                                                          )
                                                         )
                                        )
                     .exclude(approved_flag=3).order_by('time_start')
                     )
        print(result, assertion)
