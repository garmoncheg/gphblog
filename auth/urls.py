from django.conf.urls.defaults import *
from auth.views import auth_state, create_new_user

urlpatterns = patterns('',
    (r'^$', auth_state),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^create/$', create_new_user),
    (r'^profile/', auth_state),
)
