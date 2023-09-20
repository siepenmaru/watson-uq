from django import forms
from django.forms.widgets import Select
from datetime import time
from crispy_forms.helper import FormHelper

class TimeForm(forms.Form):
    date_index = forms.ChoiceField(
        choices=(
            (1, "Mon"),
            (2, "Tue"),
            (3, "Wed"),
            (4, "Thu"),
            (5, "Fri"),
            (6, "Sat"),
            (0, "Sun"),
        ), label=""
    )
    selected_time = forms.TimeField(
        label="",
        widget=Select(choices=[(time(hour, 00), f'{hour:02d}:00') for hour in range(24)])
    )
    
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
