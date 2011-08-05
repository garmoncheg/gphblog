from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import MyUserCreationForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import UserProfile
from content_grabber.views import require_flickr_auth
from django.core.urlresolvers import reverse

@login_required
def auth_state(request):
    """
    View to show user login status with redirects...
    """
    social_poster_accounts, created = UserProfile.objects.get_or_create(
                                user=request.user,
                                defaults={'user':request.user})
    ctx = {'accounts': request.user.social_auth.all(),
           'last_login': request.session.get('social_auth_last_login_backend'),
           'user': request.user,
           'social_poster_accounts':social_poster_accounts}
    return render_to_response('auth/profile.html', ctx, RequestContext(request))

@require_flickr_auth
def flickr_authentificator(request):
    #successfully authenticated by Flickr.
    return HttpResponseRedirect(reverse('profile'))


def create_new_user(request):
    """
    View to create a new user
    """
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/login/")
        else:
            return render_to_response("auth/create.html", {'form': form, })
    else:
        form = MyUserCreationForm()
    return render_to_response("auth/create.html", {'form': form, }, RequestContext(request))
