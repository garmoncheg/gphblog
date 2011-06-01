from django.contrib.syndication.feeds import Feed
from photo.models import Image

class LatestEntries(Feed):
    title = "Photoblog new posted photos."
    link = "/sitenews/"
    description = "Updates of newly posted photos in the photoblog."

#    def item_pubdate(self):
#        return Image.objects.order_by('-last_commented')[:5]
    
    def description(self, obj):
        return "Photo uploaded with title" 
    
    def items(self):
        return Image.objects.order_by('-last_commented')[:50]

