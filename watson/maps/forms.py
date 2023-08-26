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
        widget=Select(choices=[(time(hour, minute), f'{hour:02d}:{minute:02d}') for hour in range(24) for minute in range(0,60,30)])
    )
    
    helper = FormHelper()
    helper.form_class = 'form-horizontal'