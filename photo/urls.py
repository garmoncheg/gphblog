from django.conf.urls.defaults import *
from views import change_rating_ajax_view, upload_photo_ajax, thumbnail_view
from views import single_image_view, add_comment_ajax, edit_comment_ajax, delete_comment_ajax
from views import tag_edit

urlpatterns = patterns('',
    
    (r"^$", thumbnail_view),
    (r"^image/(\d+)/$", single_image_view),
    (r'^tag/(?P<tag>\w+)/$', thumbnail_view),
    
    url(r'^upload_ajax/', upload_photo_ajax, name='upload_photo_ajax'),
    
    url(r'^edit_tag/$', tag_edit, name='tag_edit'),
    
    url(r'^edit_comment/$', edit_comment_ajax, name='edit_comment'),
    url(r'^delete_comment/$', delete_comment_ajax, name='delete_comment'),
    url(r'^image/comment/$', add_comment_ajax, name='add_comment_ajax'),
    
    url(r'^image/ratingajax/', change_rating_ajax_view, name='ajaxvote'),
)
