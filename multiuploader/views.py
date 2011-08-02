from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from photo.models import Image, Album
from django.template import RequestContext

from django.core.files.uploadedfile import UploadedFile

from django.contrib.auth.decorators import login_required

from django.conf import settings

#importing json parser to generate plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail



#using logging
import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)




"""
#########################################################################################
                           photo UPLOADS
#########################################################################################
"""
@login_required
def multiupload_photo_ajax(request):
    """
    View for Uploading many photos with AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """

    if request.method == 'POST':
        log.info ('Post received')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "'+str(filename)+'"')
        #writing file directly into model
        #because we don't need form of any type.
        image = Image()
        image.user=request.user
        image.title=str(filename)
        image.image=file
        image.save()
        log.info('Uploading done')
        
        """
        generating Json response for plugin purposes
        """
        file_delete_url = 'multi_delete/'
        file_url = image.get_absolute_url()
        file_fs_name = image.image.name
        #getting thumbnail url
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url
        #generating json response
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)

        #adding photo to default album to be displayed in albums automaticly
        try:
            default_album = get_object_or_404(Album, title="User's Posted")
            image.albums.add(default_album)
        except:
            log.info('Error adding photo pk='+str(image.pk)+' to default album.')
            pass
        
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return render_to_response('multiuploader/multiuploader_main.html', {'static_url':settings.MEDIA_URL,
                                                                            'open_tv':u'{{',
                                                                            'close_tv':u'}}'}, 
                                                                context_instance=RequestContext(request))

@login_required
def multiuploader_photo_del_ajax(request, pk):
    log.info('Called delete image. Photo id='+str(pk))
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        return HttpResponseBadRequest('Only POST accepted')
    
    