from django import forms

from localflavor.gb.forms import GBPostcodeField

class ConstituencyLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Search by postcode",
        error_messages={'invalid': 'Please enter a full UK postcode'})
