from django import template
from photo.models import Image, ImageViews

register = template.Library()

@register.tag(name="register_viewer")
def do_views(parser, token):
    """ Returns view counts or none if user with this session or username 
        already viewed the photo.
        Increments Image rating and creates ImageViews model with viewing user data.
        In case no views found returns an empty string"""

    try:
        tag_name, item_pk, as_text, var_name = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments (name of the variable)" % tag_name)
    return Comments(item_pk, var_name)

class Comments(template.Node):
    def __init__(self, item_pk, var_name):
        self.item_pk = template.Variable(item_pk)
        self.var_name = var_name
    def render(self, context):
        try:
            user_key = context["request"].session.session_key
            user = context["request"].user
            image_pk = self.item_pk.resolve(context)
            try:
                #check if user viewed the image in both
                #authenticated and anonymous cases
                if user.is_authenticated():
                    ImageViews.objects.get(image__pk=image_pk, user=user)
                else:
                    ImageViews.objects.get(image__pk=image_pk, user_key=user_key)
            except ImageViews.DoesNotExist:
                #increment image views and save to base
                item_base = Image.objects.get(pk=image_pk)
                views = item_base.views
                views = views+1
                item_base.views=views
                item_base.save()
                #create unique view db entry
                if user.is_authenticated():
                    ImageViews.objects.create(image=item_base, user=user)
                else:
                    ImageViews.objects.create(image=item_base, user_key=user_key)
                context[self.var_name] = views
                print item_base.views
        except template.VariableDoesNotExist:
            return ''
        return ''
