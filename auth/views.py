from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import MyUserCreationForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def auth_state(request):
    """
    View to show user login status with redirects...
    """
    ctx = {'accounts': request.user.social_auth.all(),
           'last_login': request.session.get('social_auth_last_login_backend'),
           'user': request.user }
    return render_to_response('auth/profile.html', ctx, RequestContext(request))
    
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
