from django.contrib.auth.models import AbstractUser, Group
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

    follows = models.ManyToManyField(
        'self',  # the model with which is linked to the same User model which we refer to with 'self'
        limit_choices_to={'role': CREATOR},  # limit which users can be tracked and with the CREATOR role can be tracked
        symmetrical=False,  # there is a difference between the two actors in the relationship One user follows another
        # verbose_name='suit',
    )

    def save(self, *args, **kwargs):
        """
        Update User's save() method to add the user to the correct group
        to ensure that any new users added after migration are automatically assigned to the correct group
        based on their role Without this update to the save() method,
        only existing users at the time of migration will be correctly assigned to groups,
        and new users will have to be assigned manually.
        Automatic assignment of new users: Each time a new user is created and saved,
        they will automatically be added to the group corresponding to their role.
        Changing the role of existing users:
        If the role of an existing user is changed, the user will be added to the corresponding new group.
        """
        super().save(*args, **kwargs)
        # to override the save method in order to add new users assigned to groups automatically after migration
        if self.role == 'CREATOR':
            group = Group.objects.get(name='creators')
            if not group.user_set.filter(id=self.id).exists():
                # assign existing users in the database with the Group.user_set.add() function
                group.user_set.add(self)
        elif self.role == 'SUBSCRIBER':
            group = Group.objects.get(name='subscribers')
            if not group.user_set.filter(id=self.id).exists():
                # assign existing users in the database with the Group.user_set.add() function
                group.user_set.add(self)
