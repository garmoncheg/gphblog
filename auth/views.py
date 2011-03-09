# Create your views here.
from django.shortcuts import render_to_response
#from django.contrib.auth import authenticate #for my_auth function
from django.http import HttpResponseRedirect
from forms import MyUserCreationForm


def auth_state(request):
    if request.user.is_authenticated():
        user_auth_state = 'Logged in!'
        username = request.user.username
    else:
        user_auth_state = 'Not Logged in'
        username = 'Anonymous!'
    return render_to_response('profile.html', {'user_auth_state': user_auth_state, 'username': username})
        
def create_new_user(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/login/")
    else:
        form = MyUserCreationForm()
    return render_to_response("create.html", {
        'form': form, 
    })
