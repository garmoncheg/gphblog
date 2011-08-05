from django.db import models
#importing django User model to assign with flickr users
from django.contrib.auth.models import User


#planning to add gere method to store flickr user info upon synchronization
#from: http://www.flickr.com/services/api/flickr.people.getInfo.html
class UserProfile(models.Model):
    """Model to store user data besides standart info.
    For now it is used to include flickr auth fact"""
    user = models.ForeignKey(User)
    flickr_authenticated = models.BooleanField(default=False)
