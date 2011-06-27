from django import forms
from photo.models import Image
from django.utils.translation import ugettext_lazy as _


class UploadImageForm(forms.ModelForm):
    """
    .
    """
#    image = forms.FileField(label=_("File:"))

    class Meta:
        model = Image
        fields = ("image")
        exclude =('user','title')