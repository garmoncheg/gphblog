from django.conf.urls.defaults import *
from views import change_rating_ajax_view, upload_photo_ajax, thumbnail_view
from views import single_image_view, add_comment_ajax, edit_comment_ajax, delete_comment_ajax
from views import tag_edit, edit_title_ajax, image_rotator

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    
    (r"^$", thumbnail_view),
    (r"^image/(\d+)/$", single_image_view),
    (r'^tag/(?P<tag>\w+)/$', thumbnail_view),
    
    url(r'^rotate/', image_rotator, name='rotate'),
    url(r'^upload_ajax/', upload_photo_ajax, name='upload_photo_ajax'),
    url(r'^edit_tag/$', tag_edit, name='tag_edit'),
    url(r'^edit_title/$', edit_title_ajax, name='edit_title'),
    url(r'^edit_comment/$', edit_comment_ajax, name='edit_comment'),
    url(r'^delete_comment/$', delete_comment_ajax, name='delete_comment'),
    url(r'^image/comment/$', add_comment_ajax, name='add_comment_ajax'),
    url(r'^image/ratingajax/', change_rating_ajax_view, name='ajaxvote'),
    url(r'^about/$', direct_to_template, {'template': 'photo/about.html'}, name="about"),
)
