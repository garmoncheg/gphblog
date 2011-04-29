from django.conf.urls.defaults import *
import os.path
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^photo/', include('photo.urls')),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'photo/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('auth.urls')),
    url(r'^captcha/', include('captcha.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 
            os.path.join(settings.PROJECT_ROOT, 'media/').replace('\\','/'),
            'show_indexes': True}),
    )