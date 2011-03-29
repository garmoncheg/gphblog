# admin config here
from photo.models import Album, Tag, Image, Comment, Vote
from django.contrib import admin

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "images"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    # search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "rating", "size",
                    "tags_", "albums_", "created"]
    list_filter = ["tags", "albums", "user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["image", "author", "created", "body"]
    list_display = ["author", "created", "image"]

class VoteAdmin(admin.ModelAdmin):
    display_fields = ["image", "user", "rating"]
    list_display = ["image","cratete_date", "user", "rating"]

admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)