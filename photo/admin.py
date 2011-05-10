# admin config here
from photo.models import Album, Image, Comment, Votes, ImageViews
from django.contrib import admin

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "images"]

class ImageAdmin(admin.ModelAdmin):
    # search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "rating", "size",
                    "albums_", "created", "views"]
    list_filter = ["title", "created", "rating", "user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["image", "author", "created", "body"]
    list_display = ["author", "created", "image"]

class VotesAdmin(admin.ModelAdmin):
    display_fields = ["image", "user", "rating"]
    list_display = ["image","cratete_date", "user", "rating"]

class ImageViewsAdmin(admin.ModelAdmin):
    display_fields = ["image", "user", "user_key", "view_create_date"]
    list_display = ["image", "user", "view_create_date"]
    
admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Votes, VotesAdmin)
admin.site.register(ImageViews, ImageViewsAdmin)
