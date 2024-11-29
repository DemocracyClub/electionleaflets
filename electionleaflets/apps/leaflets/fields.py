import datetime
import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import MultiWidget

__all__ = ("DayMonthYearWidget",)

RE_DATE = re.compile(r"(\d{4})-(\d\d?)-(\d\d?)$")


class DayMonthYearWidget(MultiWidget):
    template_name = "leaflets/includes/dc_date_widget.html"
    widgets_names = ["day", "month", "year"]

    def __init__(self, attrs=None):
        self.widgets = [
            forms.NumberInput(attrs={"label": "Day", "size": 2}),
            forms.NumberInput(attrs={"label": "Month", "size": 2}),
            forms.NumberInput(attrs={"label": "Year", "size": 4}),
        ]
        super(MultiWidget, self).__init__(attrs)

    def decompress(self, value):
        if not value:
            return []
        return value


class DCDateField(forms.MultiValueField):

    widget = DayMonthYearWidget

    def __init__(self, *args, **kwargs):
        error_messages = {}

        fields = (
            forms.CharField(max_length=2),
            forms.CharField(max_length=2),
            forms.CharField(max_length=4),
        )

        super().__init__(
            error_messages=error_messages,
            fields=fields,
            require_all_fields=True,
            **kwargs
        )
        self.field_class = "form-date"

    def compress(self, data_list):
        if not data_list:
            return None
        data_list = list(data_list)
        data_list.reverse()
        return datetime.datetime(*map(int, data_list))

    def clean(self, *args, **kwargs):
        try:
            super().clean(*args, **kwargs)
            return self.compress(*args)
        except ValueError as e:
            raise ValidationError(e)
