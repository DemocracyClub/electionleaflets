from django import forms


class ReportAbuseForm(forms.Form):
    name = forms.CharField(
        max_length=50, error_messages={"required": "Please enter your name."}
    )
    email = forms.EmailField(
        max_length=100,
        error_messages={"required": "Please enter a valid email address."},
    )
    details = forms.CharField(
        max_length=500,
        widget=forms.Textarea(),
        error_messages={"required": "Please enter some details."},
    )
