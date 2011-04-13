from django import template
from photo.models import Votes

register = template.Library()

@register.tag(name="add_voted")
def do_voted(parser, token):
    """Returns a dictionary in variable 'votes_by_user' with image pk's.
       Requires "username" and items array as arguments. 
       It adds .voted property to each element in items array, depending on votes in user model.
       In case no votes found returns an empty string. """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, pk, items, as_text, var_name= token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly 2 arguments user and an item." % tag_name
    return generateVotes(pk, items, var_name)

class generateVotes(template.Node):
    def __init__(self, pk, items, var_name):
        self.pk = template.Variable(pk)
        self.items = template.Variable(items)
        self.var_name = var_name
    def render(self, context):
        try:
            user_key = context["request"].session.session_key
            user = context["request"].user
            items_array = self.items.resolve(context)
            pks = [image.pk for image in items_array]
            if user.is_authenticated():
                actual_user_pk = self.pk.resolve(context)
                user_votes = Votes.objects.filter(image__pk__in = pks, user__pk = actual_user_pk)
            else:
                user_votes = Votes.objects.filter(image__pk__in = pks, user_key = user_key)
            voted_image_pks = [vote.image.pk for vote in user_votes ]
            for item in items_array:
                if item.pk in voted_image_pks:
                    item.voted = True
                else: item.voted=False
            context[self.var_name] = items_array
        except template.VariableDoesNotExist:
            print 'Error in getting template variables. in votes_by_user'
            return ''
        return ''



