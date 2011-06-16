from django.db import models

class Tweet(models.Model):
    pub_time    = models.DateTimeField()
    twitter_id  = models.PositiveIntegerField()
    text        = models.TextField()
    user        = models.ForeignKey('TwitterUser')

    def __unicode__(self):
        return u'%s %s' % (self.user.screen_name, self.pub_time)

    def url(self):
        return u'http://twitter.com/%s/statuses/%s' % (self.user.screen_name, self.twitter_id)

class TwitterUser(models.Model):
    screen_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    location    = models.CharField(max_length=50, blank=True, null=True)
    name        = models.CharField(max_length=50, blank=True, null=True)
    thumbnail_url = models.URLField()
    url         = models.URLField(blank=True, null=True)
    friends     = models.ManyToManyField('TwitterUser', related_name='friends_user_set', blank=True, null=True)
    followers   = models.ManyToManyField('TwitterUser', related_name='followers_user_set', blank=True, null=True)

    def numFriends(self):
        return self.friends.count()

    def numFollowers(self):
        return self.followers.count()

    def __unicode__(self):
        return self.screen_name
