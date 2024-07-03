import datetime
from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    """
        To include the template context in the tag, pass the argument takes_context=True
        Let's access the template context in our custom tag,
        and use it to display either “you” or the username of the person who posted, depending on who is logged in
    """
    if user == context['user']:
        return 'you'
    return user.username


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

