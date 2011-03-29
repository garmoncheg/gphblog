from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from photo.models import Album, MEDIA_URL, Image, Comment, Vote
from django.template import RequestContext
from auth.context_processors import my_auth_processor
from forms import UploadImageForm, CommentForm
import datetime

@login_required
def add_comment_ajax(request):
    """Add a new comment.with ajax method"""
    #checking for POST
    if request.method == 'POST':
        pk = request.POST["pk"]
        author = request.user
        item = get_object_or_404(Image, pk=pk)
        comment = Comment(image=item)
        cf = CommentForm(request.POST, instance=comment)
        comment = cf.save(commit=False)
        comment.author = author
        item.last_commented = datetime.datetime.now()
        item.save()
        comment.save()
        return render_to_response("photo/comment.html", {"comment": comment})
    else:
        return HttpResponseBadRequest('Only POST accepted')

@login_required
def change_rating_ajax_view(request):
    """ A view for AJAX voting for the photo with POST method 
        and checking if user already voted"""
    if request.method == 'POST':
        pk = request.POST["pk"]
        incrementer = request.POST["incrementer"]
        user = request.user
        item = get_object_or_404(Image, pk=pk)
        intial_rating = item.rating
        #checking for whether user already voted
        try:
            #votes by request user exist
            Vote.objects.get(image = pk)
        except Vote.DoesNotExist:
            # No vote from "request.user" exists
            Vote.objects.create(image = item, user=user, rating=1)
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

@login_required
def single_image_view(request, pk):
    """Image view with rating, comments and comment form"""
    CommentForm().author = request.user
    item = get_object_or_404(Image, pk=pk)
    comments = Comment.objects.filter(image=item)
    return render_to_response("photo/image.html", {"item": item, "comments": comments, "form": CommentForm() },
                              context_instance=RequestContext(request, processors=[my_auth_processor]))

@login_required
def thumbnail_view(request):
    """Blog view, also main view"""
    item=Image.objects.all().order_by('-last_commented')
    return render_to_response("photo/main_blog.html", {'item': item },
                              context_instance=RequestContext(request, processors=[my_auth_processor]))


@login_required
def upload_photo(request):
    """View for Uploading a photo."""
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES or None)
        if form.is_valid():
            t = form.save(commit=False)
            t.user=request.user
            t.save()
            form.save_m2m()
            return HttpResponseRedirect('/photo/')
    else:
        form = UploadImageForm()
    return render_to_response("photo/upload_photo.html", {'form': form},
                              context_instance=RequestContext(request, processors=[my_auth_processor]))

def photos_by_albom(request):
    """View of photos sorted by album."""
    albums = Album.objects.all()
    if not request.user.is_authenticated():
        albums = albums.filter(public=True)

    paginator = Paginator(albums, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)

    for album in albums.object_list:
        album.images = album.image_set.all()

    return render_to_response("photo/photos_by_album.html", dict(albums=albums, user=request.user,
        media_url=MEDIA_URL), context_instance=RequestContext(request, processors=[my_auth_processor]))


