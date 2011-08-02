from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from photo.models import Image, Comment, Votes, Album
from tagging.models import Tag, TaggedItem
from django.template import RequestContext
from auth.context_processors import my_auth_processor
from forms import UploadImageForm, CommentForm, CommentFormWithCapthca
import datetime
from string import join

#notification imports for optional notification usage
from django.conf import settings
from models import User
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    notification.create_notice_type("c_add", "Comment Added", "Comment added to your photo")
    notification.create_notice_type("photo_add", "Photo Added", "user added a new photo")
else:
    notification = None


from PIL import Image as PilImage
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as thumbnails_delete
from django.contrib.auth.decorators import login_required

#temporary upon migration to new django bug fix with cs_rf
from django.views.decorators.csrf import csrf_exempt

#importing exif extractor
from photo.photo_meta import get_exif, get_exif_taken_date

#using logging
import logging
logger = logging


#using site to get our current URL
from django.contrib.sites.models import Site

#to add urls to facebook like button
import urllib



import flickrapi
"""
#########################################################################################
                           PHOTO UPLOAD TO FLICKR HANDLER
#########################################################################################
"""

@csrf_exempt
def check_for_flickr_permit(user, item, *args, **kwargs):
    """
    Function check if the user has permit to post photos to Flickr.
    """
    
    #checking for user permit to edit tags
    if user.is_authenticated():
        if (item.user==user) or (user.is_superuser):
            item.social_posting_permit = True
        else: item.social_posting_permit = False
    else:
        item.social_posting_permit = False
    return item


def flickr_callback(progress, done):
    if done:
        logger.info("Done uploading to flickr")
    else:
        logger.info( "At %s%%" % progress)

from content_grabber.views import require_flickr_auth
from django.contrib.sites.models import Site

@csrf_exempt
@login_required
def upload_to_flickr(request):
    """
    View to upload photos to Flickr
    called by POST method from user who can post his photo to flickr.
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            logger.info('Uploading photo to Flickr triggered by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    
            pk = request.POST['image_pk']
            #getting image from base
            image=get_object_or_404(Image, pk=pk)
    
            #getting image description if exists else using title instead
            if image.description:
                description = image.description
            else:
                current_site = Site.objects.get(id=1)
                description = u'Photo uploaded by Photblog website: http://'+current_site.domain+'/'
                
            #getting flickr api instance
            flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='xmlnode')
            
            #checking serve authentication
            (token,frob)= flickr.get_token_part_one(perms='write')
            flickr.get_token_part_two((token, frob))
            
            #getting file to upload path
            photo_path = settings.MEDIA_ROOT+image.image.name
            
            #generating tags string
            lst = [x[1] for x in image.tags.values_list()]
            tags = unicode(join(lst, ', '))
            
            #Uploading file
            flickr.upload( filename= str(photo_path),
                           title=image.title,
                           description=description,
                           tags = tags,
                           callback=flickr_callback,)
            logger.info('Uploaded to flickr photo id='+str(pk)+' ')
            return HttpResponse('Success posting photo to flickr!')
        else:
            logger.info('Bad request to view "post to flickr" called by user='+str(request.user))
            return HttpResponseBadRequest('Only POST accepted')
    else:
        logger.info('remote ip='+str(request.META['REMOTE_ADDR'])+' tried to access view "post to flickr"')
        return HttpResponseBadRequest('Only for authenticated users')


"""
#########################################################################################
                           IMAGE ROTATION HANDLER
#########################################################################################
"""
@csrf_exempt
@login_required
def image_rotator(request):
    logger.info('Rotate image called by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    if request.method=='POST':
        try:
            direction = request.POST["direction"]
            pk = request.POST["pk"]
        except KeyError:
            logger.error('Rotator: No image PK or direction of rotation given!')
            return HttpResponseBadRequest('No image PK or direction given!')
        else: pass
        image = get_object_or_404(Image, pk=pk)
        if (request.user.is_superuser) or (image.user==request.user):
            im = PilImage.open(image.image)
            if direction=='right':
                rotated_image = im.rotate(270)
            elif direction=='left':
                rotated_image = im.rotate(90)
            else: return HttpResponseBadRequest('Incorrect direction!')
            thumbnails_delete(image.image, delete_file=False)
            rotated_image.save(image.image.file.name, owerwrite=True)
            new_image_width=rotated_image.size[0]
            new_image_height=rotated_image.size[1]
            if (new_image_width >= new_image_height):
                thumbnail=get_thumbnail(image.image.file.name, "795x594", crop="10px 10px")
            else:
                thumbnail=get_thumbnail(image.image.file.name, "795x1094", crop="10px 10px")
            return HttpResponse(thumbnail.url)
            
        else: return HttpResponseBadRequest('You have no permission to rotate images!')
    else: return HttpResponseBadRequest('Only POST accepted!')
    

"""
#########################################################################################
                           TITLE EDITOR
#########################################################################################
"""
@csrf_exempt
def edit_title_ajax(request):
    """
    View to EDIT TITLE of an image
    """
    logger.info('TITLE edit called by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    if request.method == 'POST':
        if request.user.is_authenticated():
            action=request.POST["action"]
            if (action=="receive"):
                image_pk = request.POST["image_pk"]
                title_text = request.POST["title_text"]
                return render_to_response("title_edit/title_edit_form.html",{"pk": image_pk, "textarea_text": title_text})
            if (action=="commit"):
                image_pk = request.POST["image_pk"]
                title_body = request.POST["body"]
                if title_body == u'': 
                    return render_to_response("title_edit/title_edit_form.html",{"pk": image_pk, "textarea_text": title_text})
                else:
                    image = get_object_or_404(Image, pk=image_pk)
                    if (image.user==request.user) or (request.user.is_superuser):
                        image.title = unicode(title_body)
                        image.save()
                        return HttpResponse(unicode(title_body))
                    else:
                        return HttpResponseBadRequest('You are not allowed to edit this title!')
        else: return HttpResponseBadRequest('must be logged in to edit your photo title!')
    else:#if post
        return HttpResponseBadRequest('Only POST accepted')



"""
#########################################################################################
                           TAGS system
#########################################################################################
"""
@csrf_exempt
def get_tags_data(user, item, *args, **kwargs):
    """
    Function to retrieve tags data depending on user and add it to an image.
    """
    
    #checking for user permit to edit tags
    if user.is_authenticated():
        if (item.user==user) or (user.is_superuser):
            item.tags_permit = True
        else: item.tags_permit = False
    else:
        item.tags_permit = False
    #getting image tags
    lst = [x[1] for x in item.tags.values_list()]
    item.tags_string =unicode(join(lst, ', '))
    return item

@csrf_exempt
def tag_edit(request):
    """
    View for adding a tag
    """
    logger.info('Tag edit called by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    #POST checking
    if request.method == 'POST':
        user=request.user
        try:
            image_pk = request.POST["image_pk"]
            image=get_object_or_404(Image, pk=image_pk)
        except KeyError:
            logging.error('Can not find image specified (no request or no model instance)')
            return HttpResponseBadRequest('Can not find image specified')
        
        #checking user permit to edit tags
        if user.is_authenticated() and (image.user==user) or user.is_superuser:
            #getting tags string and parsing them with tags APP
            tag_string = request.POST["body"]
            Tag.objects.update_tags(image, tag_string)
            #generate string of tags for output
            lst = [x[1] for x in image.tags.values_list()]
            image.tags_string=unicode(join(lst, ', '))
            logger.info('updated tags for image pk='+str(image_pk)+', user='+str(user.username)+', tags string ="'+str(image.tags_string)+'"')
            return HttpResponse(unicode(image.tags_string))
        else: return HttpResponseBadRequest('Forbidden! User is not logged in!')
    else: return HttpResponseBadRequest('Only POST accepted')
    




"""
#########################################################################################
                           Comments
#########################################################################################
"""

def get_comment_form(user, *args, **kwargs):
    """
    Simple function to choose comment form depending if user is logged in.
    """
    if user.is_authenticated():
        cf = CommentForm(*args, **kwargs)
        cf.author = user
    else:
        cf = CommentFormWithCapthca(*args, **kwargs)
        cf.author = 'Anonymous'
    return cf

@csrf_exempt
def delete_comment_ajax(request):
    """
    View to DELETE comments
    """
    if request.method =='POST':
        if request.user.is_authenticated():
            comment_pk = request.POST["comment_pk"]
            comment = get_object_or_404(Comment, pk=comment_pk)
            if (comment.author==request.user) or (request.user.is_superuser):
                logger.info('Deleting comment pk='+str(comment.pk)+', user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
                comment.delete()
                return HttpResponse(comment_pk)
            else:
                return HttpResponseBadRequest('You have no permit to delete this comment!')
        else:
            return HttpResponseBadRequest('Forbidden! User is not logged in!')
    else:
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def edit_comment_ajax(request):
    """
    View to EDIT comments
    """
    logger.info('EDIT comment called user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    if request.method == 'POST':
        if request.user.is_authenticated():
            action=request.POST["action"]
            if (action=="receive"):
                comment_pk = request.POST["comment_pk"]
                comment_text = request.POST["comment_text"]
                return render_to_response("comments/comment_edit_form.html",{"pk": comment_pk, "textarea_text": comment_text})
            if (action=="comment"):
                comment_pk = request.POST["comment_pk"]
                comment_body = request.POST["body"]
                if comment_body == u'': 
                    return render_to_response("comments/comment_edit_form.html",{"pk": comment_pk, "textarea_text": comment_text})
                else:
                    comment = get_object_or_404(Comment, pk=comment_pk)
                    if (comment.author==request.user) or (request.user.is_superuser):
                        comment.body = unicode(comment_body)
                        comment.save()
                        return HttpResponse(unicode(comment.body))
                    else:
                        return HttpResponseBadRequest('You are not allowed to edit comments!')
        else: return HttpResponseBadRequest('must be logged in to edit your comments!')
    else:#if post
        return HttpResponseBadRequest('Only POST accepted')

def add_comment_ajax(request):
    """
    Add a new comment view
    """
    logger.info('ADD comment called user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    #checking for POST
    if request.method == 'POST':
        pk = request.POST["pk"]
        author = request.user
        item = get_object_or_404(Image, pk=pk)
        comment = Comment(image=item)
        cf = get_comment_form(author, data=request.POST, instance=comment)
        if cf.is_valid():
            #actions for valid comment and captcha
            comment = cf.save(commit=False)
            item.last_commented = datetime.datetime.now()
            item.save()
            if author.is_authenticated(): comment.author=author
            comment.save()
            comment.data_id = pk
            comment.permited = unicode('permit')
            logger.info('ADD comment called user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR'])+', comment='+str(comment.body))
            if notification:
                notification.send([item.user], "c_add", {"ph_title":item.title, "notice":comment.body})
            return render_to_response("comments/single_comment.html", {"comment": comment, "pk": comment.pk}, context_instance=RequestContext(request))
        else:
            #form unvalid return form with errors
            return render_to_response("comments/comment_form.html",{"comment_form": cf, "cf_pk": pk,})
        
    else:
        return render_to_response("comments/comment_form.html",{"comment_form": get_comment_form(request.user)})



"""
#########################################################################################
                           Votes(rating)
#########################################################################################
"""
@csrf_exempt
def change_rating_ajax_view(request):
    """ A view for AJAX voting for the photo with POST method 
        and checking if user already voted"""
    if request.method == 'POST':
        user_key = request.session.session_key
        pk = request.POST["pk"]
        incrementer = request.POST["incrementer"]
        user = request.user
        item = get_object_or_404(Image, pk=pk)
        intial_rating = item.rating
        #checking for whether user already voted
        try:
            #votes by request user exist
            Votes.objects.get(image = pk, user_key=user_key)
        except Votes.DoesNotExist:
            # No vote from "request.user" exists
            if request.user.is_authenticated():
                Votes.objects.create(image = item, user=user, rating=1, user_key=user_key)
            else:
                Votes.objects.create(image = item, rating=1, user_key=user_key)
            if incrementer == '1':
                #user votes "+"
                logger.info('Vote by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR'])+' +')
                item.rating = intial_rating+1
            elif incrementer == '2':
                #user votes "-"
                item.rating = intial_rating-1
                logger.info('Vote by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR'])+' -')
            item.save()
            return HttpResponse(unicode(item.rating))#if vote added correctly return image rating
        else:#try
            # User already voted.
            return HttpResponse(unicode("already voted!")) #if vote exists return error
    else:#if post
        return HttpResponseBadRequest('Only POST accepted')


"""
#########################################################################################
                           BLOG system
#########################################################################################
"""

def gallery_in_album_view(request, pk):
    """Gallery view to show images in an album"""
    logger.info('Album pk='+str(pk)+' viewed by ip='+str(request.META['REMOTE_ADDR']))
    album = get_object_or_404(Album, pk=pk)
    images = album.image_set.all()
    album.count = images.count()
    return render_to_response("photo/album_gallery.html", 
                              {"album": album,
                               "items":images,
                               "switcher":'album'},
                              context_instance=RequestContext(request))

def albums_view(request):
    """Albums view to select album to watch"""
    logger.info('Albums viewed by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    albums=Album.objects.all()
    for album in albums:
        album.images=album.image_set.all()[:4]
        album.count = album.image_set.all().count()
    return render_to_response("photo/albums_view.html", 
                              {"items": albums,
                               'tag_cloud_display': True,
                               'switcher':'album'},
                              context_instance=RequestContext(request))


def single_image_view(request, pk):
    """Image view with rating, comments and comment form"""
    logger.info('Single Image viewed by user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    user=request.user
    item = get_object_or_404(Image, pk=pk)
    
    #loading tags data from my function
    get_tags_data(user, item)
    
    #checking for user permit to post to socials
    check_for_flickr_permit(user, item)
    
    #checking for permit to edit photo title and to rotate photo
    if (item.user == request.user) or (request.user.is_superuser):
        item.title_permit = 'permit'
        item.rotation_permit=True
        
    #checking for user permit to vote
    try:
        if user.is_authenticated():
            Votes.objects.get(image__pk=pk, user=user)
        else:
            Votes.objects.get(image__pk=pk, user_key=request.session.session_key)
        item.voted = True
    except Votes.DoesNotExist: item.voted = False
    
    #generating data for facebook button
    current_site = Site.objects.get_current()
    current_domain = unicode('http://')+unicode(current_site)

    facebook_dict={"facebook_like_app_id":settings.FACEBOOK_APP_ID,
                   "facebook_user_id":settings.FACEBOOK_USER_ID,
                   "facebook_like_url":urllib.quote(current_domain+request.path),
                   "facebook_site_name":current_site
                   }
    
    # trying to load photo Exif taken DataTime
    #else using file DateTime
    image_path=settings.MEDIA_ROOT+item.image.name
    try:
        exif_date_taken=get_exif_taken_date(image_path)
        taken_date = exif_date_taken
    except:
        taken_date = 'Not provided'
        pass
    
    context = {"item": item, 
               "comment_form": get_comment_form(user),
               "facebook_dict":facebook_dict,
               "taken_date": taken_date,
               }
    return render_to_response("photo/image.html", context, context_instance=RequestContext(request))

#@login_required
def thumbnail_view(request, tag=''):
    """Blog view, also main view
    Shows 5 photos iterated by last comment.
    Also shows images for tag, if provided
    
    Includes comment and voting system for each photo."""
    logger.info('Main blog called user='+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    user = request.user
    if tag=='':
        items=Image.objects.all().order_by('-last_commented')
    else:
        tag_object = Tag.objects.get(name=tag)
        items=TaggedItem.objects.get_by_model(Image, tag_object)
        #items=Tag.objects.
    return render_to_response("photo/main_blog.html", {'items': items, 
                                                       'tagged_name': tag,
                                                       'tag_cloud_display': True,
                                                       "comment_form": get_comment_form(user),
                                                       'switcher':'blog'},
                                                        context_instance=RequestContext(request, processors=[my_auth_processor]))





"""
#########################################################################################
                           photo UPLOADS
#########################################################################################
"""

def upload_photo_ajax(request):
    """View for Uploading a photo."""
    logger.info('Single image upload called by="'+str(request.user)+', ip='+str(request.META['REMOTE_ADDR']))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = UploadImageForm(request.POST, request.FILES or None)
            if form.is_valid():
                image = form.save(commit=False)
                image.user=request.user
                image.save()
                form.save_m2m()
                try:
                    default_album = get_object_or_404(Album, title="User's Posted")
                    image.albums.add(default_album)
                except:
                    logger.info('Error adding photo pk='+str(image.pk)+' to default album.')
                    pass
                logger.info('Uploaded an image title="'+str(image.title)+', by user="'+str(request.user)+'"')
                if notification:
                    notification.send(User.objects.filter(is_superuser=True), "photo_add", {"ph_title":image.title,})

                return HttpResponse(unicode("Uploaded success!"))
            else: #form errors
                return render_to_response("photo/upload_photo_form_for_ajax.html", {'form': form})
        else: #get received
            form = UploadImageForm()
            return render_to_response("photo/upload_photo_form_for_ajax.html", {'form': form})
    else:
        return HttpResponse(unicode('<div class="phtitle">Please log in to upload photos!</div>'))


