from django import forms
from models import Image, Comment
from django.utils.translation import ugettext_lazy as _
#from recaptcha.fields import ReCaptchaField
from captcha.fields import CaptchaField


class UploadImageForm(forms.ModelForm):
    """
    A form that uploads an image to photo database into the Image Model.
    """
    title = forms.CharField(label=_("Title"), max_length=60)
    image = forms.FileField(label=_("File:"))

    class Meta:
        model = Image
        fields = ("image", "title",)
        exclude =('user',)

class CommentForm(forms.ModelForm):
    """
    A form to post comments for image instance
    """
    class Meta:
        model = Comment
        fields = ("body",)
        exclude =("author", "image")
    
    def clean_body(self):
        try:
            body= self.cleaned_data["body"]
        except:
            raise forms.ValidationError(_("You've entered some unsupported symbols. Please correct your comment"))
        return body

class CommentFormWithCapthca(forms.ModelForm):
    """
    A form to post comments for image instance
    """
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ("body","captcha",)
        exclude =("author", "image")