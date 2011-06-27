from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from photo.models import Image, Comment, Votes
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


"""
#########################################################################################
                           TITLE EDITOR
#########################################################################################
"""

def edit_title_ajax(request):
    """
    View to EDIT TITLE of an image
    """
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
        print 'get recieved'
        return HttpResponseBadRequest('Only POST accepted')



"""
#########################################################################################
                           TAGS system
#########################################################################################
"""
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


def tag_edit(request):
    """
    View for adding a tag
    """
    #POST checking
    if request.method == 'POST':
        user=request.user
        image_pk = request.POST["image_pk"]
        image=get_object_or_404(Image, pk=image_pk)
        #checking user permit to edit tags
        if user.is_authenticated() and (image.user==user) or user.is_superuser:
            #getting tags string and parsing them with tags APP
            tag_string = request.POST["body"]
            Tag.objects.update_tags(image, tag_string)
            #generate string of tags for output
            lst = [x[1] for x in image.tags.values_list()]
            image.tags_string=unicode(join(lst, ', '))
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

def delete_comment_ajax(request):
    """
    View to DELETE comments
    """
    if request.method =='POST':
        if request.user.is_authenticated():
            comment_pk = request.POST["comment_pk"]
            comment = get_object_or_404(Comment, pk=comment_pk)
            if (comment.author==request.user) or (request.user.is_superuser):
                comment.delete()
                return HttpResponse(comment_pk)
            else:
                return HttpResponseBadRequest('You have no permit to delete this comment!')
        else:
            return HttpResponseBadRequest('Forbidden! User is not logged in!')
    else:
        return HttpResponseBadRequest('Only POST accepted')

def edit_comment_ajax(request):
    """
    View to EDIT comments
    """
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
                item.rating = intial_rating+1
            elif incrementer == '2':
                #user votes "-"
                item.rating = intial_rating-1
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
def single_image_view(request, pk):
    """Image view with rating, comments and comment form"""
    user=request.user
    item = get_object_or_404(Image, pk=pk)
    
    #loading tags data from my function
    get_tags_data(user, item)
    
    #checking for permit to edit photo title
    if (item.user == request.user) or (request.user.is_superuser):
        item.title_permit = 'permit'
    else: print 'oshibochka!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    
    #checking for user permit to vote
    try:
        if user.is_authenticated():
            Votes.objects.get(image__pk=pk, user=user)
        else:
            Votes.objects.get(image__pk=pk, user_key=request.session.session_key)
        item.voted = True
    except Votes.DoesNotExist: item.voted = False
    
    return render_to_response("photo/image.html", {"item": item, "comment_form": get_comment_form(user), },
                              context_instance=RequestContext(request))

#@login_required
def thumbnail_view(request, tag=''):
    """Blog view, also main view"""
    user = request.user
    if tag=='':
        items=Image.objects.all().order_by('-last_commented')
    else:
        tag_object = Tag.objects.get(name=tag)
        items=TaggedItem.objects.get_by_model(Image, tag_object)
        #items=Tag.objects.
    return render_to_response("photo/main_blog.html", {'items': items, 
                                                       'tagged_name': tag,
                                                       "comment_form": get_comment_form(user),},
                                                        context_instance=RequestContext(request, processors=[my_auth_processor]))





"""
#########################################################################################
                           photo UPLOADS
#########################################################################################
"""

def upload_photo_ajax(request):
    """View for Uploading a photo."""
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = UploadImageForm(request.POST, request.FILES or None)
            if form.is_valid():
                image = form.save(commit=False)
                image.user=request.user
                image.save()
                form.save_m2m()
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


