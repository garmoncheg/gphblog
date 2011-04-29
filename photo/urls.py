from django.conf.urls.defaults import *
from views import change_rating_ajax_view, upload_photo_ajax, thumbnail_view
from views import single_image_view, add_comment_ajax

urlpatterns = patterns('',
    (r"^$", thumbnail_view),
    url(r'^upload_ajax/', upload_photo_ajax, name='upload_photo_ajax'),
    (r"^image/(\d+)/$", single_image_view),
    url(r'^image/comment/$', add_comment_ajax, name='add_comment_ajax'),
    url(r'^image/ratingajax/', change_rating_ajax_view, name='ajaxvote'),
)
