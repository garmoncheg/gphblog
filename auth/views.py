from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import MyUserCreationForm

def auth_state(request):
    """
    View to show user login status with redirects...
    """
    if request.user.is_authenticated():
        user_auth_state = 'Logged in!'
        username = request.user.username
    else:
        user_auth_state = 'Not Logged in'
        username = 'Anonymous!'
    return render_to_response('auth/profile.html', {'user_auth_state': user_auth_state, 'username': username})
        
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
        form = MyUserCreationForm()
    return render_to_response("auth/create.html", {
        'form': form, 
    })
