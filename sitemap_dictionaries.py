from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from photo.models import Image

#sitemaps data
info_dict = {
    'queryset': Image.objects.all(),
    'date_field': 'last_commented',
}
sitemaps = {
    #'flatpages': FlatPageSitemap,
    'blog': GenericSitemap(info_dict, priority=0.6),
}