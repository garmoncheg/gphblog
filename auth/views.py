from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import MyUserCreationForm

def auth_state(request):
    """
    View to show user login status with redirects...
    """
    user=request.user
    return render_to_response('auth/profile.html', {'user': user})
    
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
    return render_to_response("auth/create.html", {'form': form, })
