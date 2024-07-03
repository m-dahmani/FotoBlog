from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def model_type(value):
    """
    To return a string representation of the model type to which the instance belongs
    """
    return type(value).__name__  # value.__class__.__name__


@register.filter
def get_posted_at_display(post_time):
    """ displays a dynamic string based on the date a post was added"""
    now = timezone.now()
    # Calculation of time difference: We calculate the difference between the current moment and the post creation time
    diff = now - post_time

    minutes = int(diff.total_seconds() / 60)
    hours = int(diff.total_seconds() / 3600)

    # Conditions: We check if the difference is less than 60 minutes, between 1 and 24 hours, or greater than 24 hours,
    # and return an appropriate string.
    if minutes < 60:
        return f"Posté il y a {minutes} minutes"
    elif hours < 24:
        return f"Posté il y a {hours} heures"
    else:
        # Date formatting: If the difference is more than 24 hours, we use strftime to format the date in a readable way
        return post_time.strftime("Posté à %H:%M %d %b %y")


@register.filter(name='uppercase')
def uppercase(value):
    """Convert a string into all uppercase."""
    return value.upper()
