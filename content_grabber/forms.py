from django import forms
from django.utils.translation import ugettext_lazy as _


class GrabFlickrByUsername(forms.Form):
    """
    A form for grabbing user photos by flickr Username.
    """
    flickr_username = forms.CharField(label=_("Flickr Username"), max_length=60)


