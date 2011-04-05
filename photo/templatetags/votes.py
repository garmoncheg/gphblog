from django import template
from photo.models import Vote

register = template.Library()

@register.tag(name="add_voted")
def do_voted(parser, token):
    """Returns a dictionary in variable 'votes_by_user' with image pk's.
       Requires "username" and items array as arguments. 
       It adds .voted property to each element in items array, depending on votes in user model.
       In case no votes found returns an empty string. """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, pk, items = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly 2 arguments user and an item." % token.contents.split()[0]
    return Votes(pk, items)

class Votes(template.Node):
    def __init__(self, pk, items):
        self.pk = template.Variable(pk)
        self.items = template.Variable(items)
        
    def render(self, context):
        try:
            actual_pk = self.pk.resolve(context)
            items_array = self.items.resolve(context)
            pks = [image.pk for image in items_array]
            user_votes = Vote.objects.filter(image__pk__in = pks, user__pk = actual_pk)
            voted_image_pks = [vote.image.pk for vote in user_votes ]
            for item in items_array:
                if item.pk in voted_image_pks:
                    item.voted = True
                else: item.voted=False
            context['items'] = items_array
        except template.VariableDoesNotExist:
            return ''
        return ''



