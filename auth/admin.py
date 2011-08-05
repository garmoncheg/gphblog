# admin config here
from models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ["user", "flickr_authenticated"]
    list_display = ["user", "flickr_authenticated"]
    display_fields = ["user", "flickr_authenticated"]
    
admin.site.register(UserProfile, UserProfileAdmin)

