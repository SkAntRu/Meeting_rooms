from datetime import datetime, date, time, timedelta
from django.contrib.auth import get_user_model
from django.db import models
import pytz
from django.conf import settings


cur_utc = pytz.timezone(settings.TIME_ZONE)


class MeetingRoom(models.Model):
    """Class MeetingRoom

    Attributes:
        meeting_room_name
        amount_of_chairs
        projector:bool
        flip_chart:bool
        description

    Definitions:
        first_bid(self)
    Return all bids relative to current meeting room

        all_bids(self)
    Return all bids relative to current meeting room
    """
    meeting_room_name = models.CharField('Комната переговоров', max_length=10,
                                         db_index=True,
                                         unique=True,
                                         primary_key=True,
                                         )
    amount_of_chairs = models.PositiveIntegerField('Количество стульев', default=0)
    projector = models.BooleanField('Проектор', default=0)
    flip_chart = models.BooleanField('Флипчарт', default=0)
    description = models.CharField('Описание переговорной', max_length=200, default='')

    def __str__(self):
        return str(self.meeting_room_name)

    def first_bid(self):
        """Return first time approaching bid"""
        try:
            first_bid = (Bid.objects.filter(meeting_room=self,
                                            time_end__range=(datetime.utcnow().replace(tzinfo=cur_utc),
                                                             datetime.combine(date.today(),
                                                                              time(23, 59).replace(tzinfo=cur_utc)
                                                                              )
                                                             )
                                            )
                         .exclude(approved_flag=3).order_by('time_start')
                         )[0]
        except IndexError:
            first_bid = ''
        return first_bid

    def all_bids(self, current_day_flag=False):
        """Return all bids relative to current meeting room"""
        all_bids = (Bid.objects.filter(meeting_room=self,
                                       time_end__range=(datetime.utcnow().replace(tzinfo=cur_utc),
                                                        (datetime.combine(date.today(),
                                                                          time(23, 59).replace(tzinfo=cur_utc)
                                                                          )
                                                        if current_day_flag else
                                                        datetime.utcnow().replace(tzinfo=cur_utc)+timedelta(weeks=1)
                                                         )
                                                        )
                                       )
                    .exclude(approved_flag=3).order_by('time_start')
                    )

        return all_bids

    class Meta:
        permissions = (
            ('change', 'Может изменять атрибутивный состав переговорных'),
        )
        verbose_name = 'Переговорная'
        verbose_name_plural = 'Переговорные'


class Bid(models.Model):
    """Class Bid

    Attributes:
        meeting_room
        time_start
        time_end
        author
        approved_flag
        reserved_time
        reserved_date
        comment

    Definitions:
        @staticmethod
        get_awaiting_solution_bids()
    Return set of bid with status 1:'Under consideration'

        accept_bid(self):
    Accept Bid

        refuse_bid(self):
    Refuse Bid

    """
    User = get_user_model()

    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, default='0')
    time_start = models.DateTimeField('Дата начала', auto_now=False, auto_now_add=False, default=None,)
    time_end = models.DateTimeField('Дата окончания', auto_now=False, auto_now_add=False, default=None,)
    author = models.ForeignKey(User, verbose_name='Автор заявки', on_delete=models.CASCADE,)
    _status = (
        (1, 'На рассмотрении'),
        (2, 'Одобрено'),
        (3, 'Отказано'),
    )
    approved_flag = models.PositiveSmallIntegerField(
        'Статус',
        choices=_status,
        default=1,
    )
    reserved_time = models.CharField('Время бронирования', max_length=11, default='', blank=True)
    reserved_date = models.CharField('Дата бронирования', max_length=12, default='', blank=True)
    comment = models.CharField('Комментарий', max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.reserved_time = (
                str(self.time_start.strftime("%H:%M"))
                + '-' +
                str(self.time_end.strftime("%H:%M"))
        )
        self.reserved_date = (
            str(self.time_end.strftime("%d.%m.%Y"))
        )
        super(Bid, self).save(*args, **kwargs)

    @staticmethod
    def get_awaiting_solution_bids():
        """Return set of bid with status 1:'Under consideration'"""
        awaiting_solution_bids = (Bid.objects.filter(approved_flag=1,
                                                     time_start__range=(
                                                         datetime.utcnow().replace(tzinfo=cur_utc),
                                                         datetime.utcnow().replace(tzinfo=cur_utc)+timedelta(weeks=1)
                                                     )
                                                     )
                                  ).order_by('time_start')
        return awaiting_solution_bids

    def __str__(self):
        return str(self.id)

    def accept_bid(self):
        """Accept Bid"""
        self.approved_flag = 2
        super(Bid, self).save()

    def refuse_bid(self):
        """Refuse Bid"""
        self.approved_flag = 3
        super(Bid, self).save()

    class Meta:
        permissions = (
            ('accept_decline_bid', 'Может подтверждать заявки'),
        )
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
