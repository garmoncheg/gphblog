from django.conf.urls.defaults import *
from views import  photos_by_albom, upload_photo, thumbnail_view
from views import single_image_view, change_photo_rating_view, add_comment

urlpatterns = patterns('',
    # Example:
    # (r'^gphblog/', include('gphblog.foo.urls')),
    #(r"^blog/(comment|post)/$", "thumbnail_view"),
    (r"^$", thumbnail_view),
    (r"^albums/$", photos_by_albom),
    (r"^upload/", upload_photo),
    (r"^image/(\d+)/$", single_image_view),
    (r"^image/rating/(\d+)/(\d+)/$", change_photo_rating_view),
    (r"^image/(\d+)/comment/$", add_comment),
    #(r"^(\d+)/(comment|post)/$", "album"),
)
