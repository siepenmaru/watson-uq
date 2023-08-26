from django import forms
from django.forms.widgets import Select
from datetime import time

class TimeForm(forms.Form):
    selected_time = forms.TimeField(
        widget=Select(choices=[(time(hour, minute), f'{hour:02d}:{minute:02d}') for hour in range(24) for minute in range(0,60,30)])
    )