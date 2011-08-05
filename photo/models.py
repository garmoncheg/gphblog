from django.db import models
from django.contrib.auth.models import User
from string import join
import os
from PIL import Image as PilImage
from settings import MEDIA_ROOT, MEDIA_URL 

import tagging

from syncr.flickr.models import FLICKR_LICENSES

class Album(models.Model):
    """Album used to store photos. Has "Public" key """
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    
    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='/site_media/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    images.allow_tags = True
    
    def __unicode__(self):
        return self.title

class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_commented = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    views = models.IntegerField(default=0)
    description = models.TextField(max_length=800, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PilImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        super(Image, self).save(*args, ** kwargs)
        
    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))
    
    def fullpath(self):
        return "%s" % ((MEDIA_URL + self.image.name))
    
    @models.permalink
    def get_absolute_url(self):
        return ('photo.views.single_image_view', [str(self.pk)])
    
    def thumbnail(self):
        return """<a href="/site_media/%s">%s</a>""" % ((self.image.name, self.image.name))
    thumbnail.allow_tags = True

#registering tagging model to access some handy tags managers 
tagging.register(Image)

class Comment(models.Model):
    """Single comment model. Returns comment"""
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, blank=True)
    body = models.TextField()
    image = models.ForeignKey(Image)

    def __unicode__(self):
        return unicode("%s: %s" % (self.author, self.body[:60]))

class Votes(models.Model):
    """Model for storing votes of users for the photo"""
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User, null=True, blank=True)
    user_key = models.CharField(max_length=40, null=True, blank=True)
    cratete_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    class Meta:
        unique_together = (("image", "user"),)

    def __unicode__(self):
        return unicode(self.image.pk)

class ImageViews(models.Model):
    """Model for storing unique views of users.
    Used in templatetag created for returning user Views for every photo."""
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User, null=True, blank=True)
    user_key = models.CharField(max_length=40)
    view_create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return unicode(self.image.pk)

class SocialPost(models.Model):
    """Model to store user posts of photos to social Web sites.
    Saves user posts to:
    - Flickr
    """
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    flickr=models.BooleanField(default=True)