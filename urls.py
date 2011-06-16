from django.conf.urls.defaults import *
import os.path
from django.conf import settings
from django.contrib import admin
from feeds.feeds import LatestEntries
from sitemap_dictionaries import sitemaps

admin.autodiscover()

#feeds data
feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
    (r'^photo/', include('photo.urls')),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'photo/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('auth.urls')),
    (r'^content/', include('content_grabber.urls')),
    (r'^notification/', include('notification.urls')),
    url(r'^captcha/', include('captcha.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 
            os.path.join(settings.PROJECT_ROOT, 'media/').replace('\\','/'),
            'show_indexes': True}),
    )