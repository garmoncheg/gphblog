# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from photo.models import Album, MEDIA_URL, Image, Comment
from django.template import RequestContext
from auth.context_processors import my_auth_processor
from forms import UploadImageForm, CommentForm
import datetime

@login_required
def add_comment(request, pk):
    """Add a new comment."""
    comment = Comment(image=Image.objects.get(pk=pk))
    cf = CommentForm(request.POST, instance=comment)
    comment = cf.save(commit=False)
    comment.author = request.user
    item = Image.objects.get(pk=pk)
    item.last_commented = datetime.datetime.now()
    item.save()
    comment.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def change_photo_rating_view(request, incrementer, pk):
    """ A view for voting for the photo """
    item = Image.objects.get(pk=pk)
    if incrementer == '1':
        item.rating = item.rating+1
    else:
        item.rating = item.rating-1
    item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def single_image_view(request, pk):
    """Image view with rating, comments and comment form"""
    item = Image.objects.get(pk=pk)
    comments = Comment.objects.filter(image=item)
    return render_to_response("photo/image.html", {"item": item, "comments": comments, "form": CommentForm() },
                              context_instance=RequestContext(request, processors=[my_auth_processor]))

@login_required
def thumbnail_view(request):
    """Blog view, also main view"""
#    item=Image.objects.all().order_by(Comment('-created'))
#    if view == "post":
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


