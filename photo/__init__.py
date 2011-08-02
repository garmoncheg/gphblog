from django.db.models.signals import post_syncdb
import models
from models import Album

def create_first_album(sender, **kwargs):
    """
    Create your album sequence to create default album to post photos to
    checks for existence of this album and creates one if no given.
    """
    # Your specific logic here
    obj, created = Album.objects.get_or_create(title="User's Posted", public=True)
    if created:
        print("Created album 'User's Posted'. Needed for storing basic photos.")
    else: 
        print("NOT CRATED album 'User's Posted'.")
    pass

post_syncdb.connect(create_first_album, sender=models)