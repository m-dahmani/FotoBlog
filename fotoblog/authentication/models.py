from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # we want to include all functionality of the User class by default
    
    CREATOR = 'CREATOR'  # check the value of the role field without hardwriting the value if user.role == user.CREATOR
    SUBSCRIBER = 'SUBSCRIBER'
    
    ROLE_CHOICES = (
        (CREATOR, 'Creator'),
        (SUBSCRIBER, 'Subscriber'),
    )
    # extend AbstractUser and add two more fields
    profile_photo = models.ImageField(verbose_name='Profile picture')
    role = models.CharField(choices=ROLE_CHOICES, max_length=30, verbose_name='Role')

