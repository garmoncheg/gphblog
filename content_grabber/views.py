from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
# for using login required view decorator
from django.contrib.auth.decorators import login_required


#form for choosing username for flickr import
from content_grabber.forms import GrabFlickrByUsername

#for using flickrapi
import flickrapi
from django.conf import settings

#using logging in flickr auth views
import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# for using django-syncr
from syncr.app.flickr import FlickrSyncr

#using django syncr Models of synced photos
from syncr.flickr.models import *

from photo.models import Image
"""
#########################################################################################
                           Flickr authentication
#########################################################################################
"""
def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''

    def protected_view(request, *args, **kwargs):
        if 'token' in request.session:
            token = request.session['token']
            log.info('Getting token from session: %s' % token)
        else:
            token = None
            log.info('No token in session')

        f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
               settings.FLICKR_API_SECRET, token=token,
               store_token=False)

        if token:
            # We have a token, but it might not be valid
            log.info('Verifying token')
            try:
                f.auth_checkToken()
            except flickrapi.FlickrError:
                token = None
                del request.session['token']

        if not token:
            # No valid token, so redirect to Flickr
            log.info('Redirecting user to Flickr to get frob')
            url = f.web_login_url(perms='read')
            return HttpResponseRedirect(url)

        # If the token is valid, we can call the decorated view.
        log.info('Token is valid')

        return view(request, *args, **kwargs)

    return protected_view

def callback(request):
    if request.method == 'GET':
        log.info('We got a callback from Flickr, store the token')

        f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
            settings.FLICKR_API_SECRET, store_token=False)

        frob = request.GET['frob']
        token = f.get_token(frob)
        request.session['token'] = token

        return HttpResponseRedirect(reverse('flickr_synchronize_second_phase'))
    else:
        return HttpResponseBadRequest('only GET Accepted')

@require_flickr_auth
def flickr_auth_test(request):
    return render_to_response('cgbflickr/cgb_flickr_done1.html', {'user': request.user, })



"""
#########################################################################################
                           Flickr synchronization
#########################################################################################
"""
@login_required
def flickr_synchronize(request):
    if request.method == 'GET':
        return render_to_response('cgbflickr/cgb_flickr.html', {'user': request.user, })
    elif request.method == 'POST':
        return HttpResponse('POST flickr syncronization view not accepted')

@login_required
@require_flickr_auth
def flickr_synchronize2(request):
    if request.method == 'POST':
        form_username = GrabFlickrByUsername(request.POST)
        #flag = request.POST == ['choice']
        
        if form_username.is_valid():
            
            flickr_syncr_instance = FlickrSyncr(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET)
            flickr_username = request.POST["flickr_username"]
            log.info( 'FlickrSync by user name: "' + flickr_username + '" submitted. '+
            'It will sync All Photo Sets of '+ flickr_username )
            try:
                flickr_syncr_instance.syncAllPhotoSets(flickr_username)
            except AttributeError:
                errors = 'Error! Username "'+flickr_username+'" has no photosets or photos!'
                log.info('Sync for user "'+flickr_username+'" has failed')
                return render_to_response ('cgbflickr/cgb_flickr2.html', {'user': request.user,
                                                                 'form':form_username,
                                                                 'errors':errors,
                                                                 })
        else:
            return render_to_response('cgbflickr/cgb_flickr2.html', {'user': request.user,
                                                                 'form':form_username,
                                                                 })

        flickr_photos = Photo.objects.all().order_by('-upload_date')#list of photos got
        flickr_photos_count = flickr_photos.count()
                                                                #change user to flickr user data
        return render_to_response('cgbflickr/cgb_flickr3.html', {'user': request.user,
                                                                 'flickr_photos': flickr_photos,
                                                                 'flickr_photos_count':flickr_photos_count,
                                                                 })
    else:
        form_username = GrabFlickrByUsername()# An unbound form
        return render_to_response('cgbflickr/cgb_flickr2.html', {'user': request.user,
                                                                 'form': form_username,
                                                                 })




import urllib2
from urlparse import urlparse
from django.core.files.base import ContentFile

@login_required
@require_flickr_auth
def flickr_synchronize3(request):
    
    flickr_photos = Photo.objects.all()
    list = '' #list to log photos to      feature request in future versions!
    for photo in flickr_photos:
        log.info('Adding photo "'+str(photo.flickr_id)+'" to main Photoblog database table')
        
        photo_url = photo.get_large_url()
        log.info('Trying to download photo from url: "'+str(photo_url)+'"')
        name = urlparse(photo_url).path.split('/')[-1]
        content = ContentFile(urllib2.urlopen(photo_url).read())
        image=Image()
        image.image.save(name=name, content=content, save=True)
        image.title=photo.title
        image.user=request.user
        image.save()
        photo.delete()
        list = list+str(photo.flickr_id)+','
    return HttpResponse('Flickr sync completed! <a href="/">Go home<a>')









"""
#########################################################################################
                           Main content grabber
#########################################################################################
"""
@login_required
def cgbmain(request):
    if request.method == 'GET':
        return render_to_response('cgbmain/cgb_main.html', {'user': request.user,
                                                            })


