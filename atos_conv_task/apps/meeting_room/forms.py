from django.forms import ModelForm
from django import forms
from .models import Bid, MeetingRoom
from datetime import datetime as dtt
import pytz
from django.conf import settings

cur_utc = pytz.timezone(settings.TIME_ZONE)


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ('meeting_room',
                  'author',
                  'time_start',
                  'time_end'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['meeting_room'].widget = forms.HiddenInput()
        self.fields["time_start"].widget = DateTimeInput()
        self.fields['time_end'].widget = DateTimeInput()
        self.fields["time_start"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields['time_end'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

    def clean(self):
        cleaned_data = super().clean()
        time_start = cleaned_data.get("time_start")
        time_end = cleaned_data.get("time_end")
        if time_start > time_end:
            raise forms.ValidationError(
                'Дата окончания - {0} должна быть старше даты начала {1}'.format(time_end.strftime("%H:%M"),
                                                                                 time_start.strftime("%H:%M")),
            )
        elif time_start < dtt.utcnow().replace(tzinfo=cur_utc):
            raise forms.ValidationError(
                'Не за чем бронировать переговорную в прошедшем времени',
            )
        elif time_start.date() != time_end.date():
            raise forms.ValidationError(
                'Просьба указывать время бронирования в рамках одного календарного дня',
            )
        # Check if Bid already registered at selected time
        current_room = cleaned_data.get('meeting_room')
        registered_bids = current_room.all_bids()
        if registered_bids:
            for bid in registered_bids:
                if bid.time_start <= time_start < bid.time_end or bid.time_start < time_end <= bid.time_end:
                    raise forms.ValidationError(
                        'На это время переговорная уже имеет оформленную заявку, просим выбрать другой период',
                    )


class CustomizeRoom(ModelForm):
    class Meta:
        model = MeetingRoom
        fields = ('meeting_room_name',
                  'amount_of_chairs',
                  'projector',
                  'flip_chart',
                  'description'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting_room_name'].widget = forms.HiddenInput()
