from django import forms
from app.models import Statement
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import datetime


class StatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = [
            'first_name',
            'username',
            'last_name',
            'auto_mark',
            'manager',
            'date',
            'time',
        ]

    date = forms.DateField(
        required=True,
        label="Дата",
        widget=DatePickerInput(
            options={
                "daysOfWeekDisabled": [0, 6],
                "locale": "ru",
                "showClose": True,
                "showClear": False,
                "showTodayButton": False,
            }
        ).start_of('event days')
    )
    time = forms.CharField(
        required=True,
        label="Время",
        widget=TimePickerInput(
            options={
                "minDate": (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'),
                "maxDate": (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d 23:59:59'),
                "enabledHours": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                "format": "H:00",
                "locale": "ru",
                "showClose": True,
                "showClear": False,
                "showTodayButton": False,
            }
        ),
    )

    def clean(self):
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        manager = self.cleaned_data.get('manager')
        all_hours = [
            "10:00", "11:00", "12:00",
            "13:00", "14:00", "15:00",
            "16:00", "17:00", "18:00",
            "19:00", "20:00"
        ]
        unavailable_time = Statement.objects.filter(manager=manager, date=date)
        unavailable_hours = []
        for record in unavailable_time:
                unavailable_hours.append(record.time)
        available_hours = [x for x in all_hours if x not in unavailable_hours]
        error = " ,".join(available_hours)
        if Statement.objects.filter(manager=manager, date=date, time=time).exists():
            raise forms.ValidationError(
                """
                Извините но данное время у выбранного вами менеджера уже занято, 
                вы можете записаться на следующие часы: {}
                """.format(error)
            )
        return self.cleaned_data
