from django import forms

from localflavor.gb.forms import GBPostcodeField

class ConstituencyLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Enter your postcode")
