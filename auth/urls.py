from django.conf.urls.defaults import *
from auth.views import auth_state, create_new_user

urlpatterns = patterns('',
    (r'^$', auth_state),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'auth/logout.html'}),
    (r'^create/$', create_new_user),
    url(r'^profile/', auth_state, name='profile'),
    url(r'^test_flickr_auth/$', 'auth.views.flickr_authentificator', name='flickr_authentificate'),
)
