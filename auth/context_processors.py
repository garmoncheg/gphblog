def my_auth_processor(request):
    #My authentication context processor
    "A context processor that provides 'app', 'user' and 'ip_adress'."
    return{
           'appname': 'Photoblog',
           'current_user': request.user,
           'ip_adress': request.META['REMOTE_ADDR'],
           }
