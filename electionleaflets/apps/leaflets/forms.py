from django import forms

from localflavor.gb.forms import GBPostcodeField

class ImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'accept': "image/*;capture=camera"}))

class FrontPageImageForm(ImageForm):
    pass

class BackPageImageForm(ImageForm):
    pass

class InsidePageImageForm(ImageForm):
    pass

class PostcodeForm(forms.Form):
    postcode = GBPostcodeField()





