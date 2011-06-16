from django.conf.urls.defaults import *
from views import cgbmain, flickr_synchronize, flickr_auth_test, callback, flickr_synchronize2, flickr_synchronize3

urlpatterns = patterns('',
    url(r'^$', cgbmain, name='cgbmain'),
    url(r'^flickr_sync/$', flickr_synchronize, name='flickr_synchronize'),
    url(r'^test_flickr_login/$', flickr_auth_test, name='flickr_auth_test'),
    url(r'^callback/$', callback, name='callback'),
    url(r'^flickr_sync2/$', flickr_synchronize2, name='flickr_synchronize_second_phase'),
    url(r'^flickr_sync3/$', flickr_synchronize3, name='flickr_synchronize_finale'),
)
