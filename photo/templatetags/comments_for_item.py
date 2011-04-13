from django import template
from photo.models import Comment

register = template.Library()

@register.tag(name="add_comments_for_item")
def do_comments(parser, token):
    """
    Returns certain amount of comments for item.
    Requires "item", amount of comments, and a variable name
    in format 123 as 4. For example:
    {% add_comments_for_item item 300 as comments %}"""
    try:
        tag_name, item, comments_amount, as_text, var_name = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % tag_name)
    return Comments(item, comments_amount, var_name)

class Comments(template.Node):
    def __init__(self, item, comments_amount, var_name):
        self.item = template.Variable(item)
        self.comments_amount = comments_amount
        self.var_name = var_name
    def render(self, context):
        try:
            item = self.item.resolve(context)
            comments = Comment.objects.filter(image=item).order_by('-created')[:self.comments_amount]
            context[self.var_name] = comments
        except template.VariableDoesNotExist:
            return ''
        return ''
