from django.db import models
from tagging.fields import TagField

class Bookmark(models.Model):
    # description, href, tags, extended, dt
    description = models.CharField(max_length=250, blank=True)
    url = models.URLField(unique=True)
    tags = TagField()
    extended_info = models.TextField(blank=True)
    post_hash = models.CharField(max_length=100)
    saved_date = models.DateTimeField()

    class Meta:
        ordering = ('-saved_date',)
        get_latest_by = 'saved_date'

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        return ('bookmark_detail', (), { 'year': self.saved_date.strftime('%Y'),
                                         'month': self.saved_date.strftime('%m'),
                                         'day': self.saved_date.strftime('%d'),
                                         'object_id': self.id })
