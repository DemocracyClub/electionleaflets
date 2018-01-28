from django import forms
from django.utils.translation import ugettext as _

from core.helpers import geocode

from localflavor.gb.forms import GBPostcodeField


class ConstituencyLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Search by postcode",
                               error_messages={'invalid': 'Please enter a full UK postcode'})
    location = None

    def clean(self):
        cleaned_data = super(ConstituencyLookupForm, self).clean()
        pcode = cleaned_data.get("postcode")
        self.location = geocode(pcode)
        if not self.location:
            raise forms.ValidationError(_("That postcode was not found. Please try another"))
