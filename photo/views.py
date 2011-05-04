from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from photo.models import Image, Comment, Votes
from django.template import RequestContext
from auth.context_processors import my_auth_processor
from forms import UploadImageForm, CommentForm, CommentFormWithCapthca
import datetime

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
    View to edit comments
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

#@login_required
def add_comment_ajax(request):
    """Add a new comment.with ajax method"""
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
            return render_to_response("comments/single_comment.html", {"comment": comment, "pk": comment.pk}, context_instance=RequestContext(request))
        else:
            #form unvalid return form with errors
            return render_to_response("comments/comment_form.html",{"comment_form": cf, "cf_pk": pk,})
        
    else:
        return render_to_response("comments/comment_form.html",{"comment_form": get_comment_form(request.user)})

#@login_required
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

#@login_required
def single_image_view(request, pk):
    """Image view with rating, comments and comment form"""
    user=request.user
    item = get_object_or_404(Image, pk=pk)
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
def thumbnail_view(request):
    """Blog view, also main view"""
    user = request.user
    items=Image.objects.all().order_by('-last_commented')
    return render_to_response("photo/main_blog.html", {'items': items, 
                                                       "comment_form": get_comment_form(user),},
                                                        context_instance=RequestContext(request, processors=[my_auth_processor]))

#@login_required
def upload_photo_ajax(request):
    """View for Uploading a photo."""
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = UploadImageForm(request.POST, request.FILES or None)
            if form.is_valid():
                t = form.save(commit=False)
                t.user=request.user
                t.save()
                form.save_m2m()
                return HttpResponse(unicode("Uploaded success!"))
            else: #form errors
                return render_to_response("photo/upload_photo_form_for_ajax.html", {'form': form})
        else: #get received
            form = UploadImageForm()
            return render_to_response("photo/upload_photo_form_for_ajax.html", {'form': form})
    else:
        return HttpResponse(unicode('<div class="phtitle">Please log in to upload photos!</div>'))


