from django.db import models
#importing django User model to assign with flickr users
from django.contrib.auth.models import User


#planning to add gere method to store flickr user info upon synchronization
#from: http://www.flickr.com/services/api/flickr.people.getInfo.html
class FlickrUser(models.Model):
    flickr_id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    flickr_username = models.CharField(max_length=50)
    flickr_user_loacation = models.CharField(max_length=200, blank=True)
    flickr_user_photos_count = models.PositiveIntegerField()