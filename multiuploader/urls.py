from django.conf.urls.defaults import *
from views import multiupload_photo_ajax, multiuploader_photo_del_ajax


urlpatterns = patterns('',
    (r"^multi_delete/(\d+)/$", multiuploader_photo_del_ajax),
    url(r"^$", multiupload_photo_ajax, name="multi_upload_photo_ajax"),
    
)
