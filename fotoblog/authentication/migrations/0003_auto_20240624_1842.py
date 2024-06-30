# Generated by Django 4.2.13 on 2024-06-24 18:42
from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def create_groups(apps, schema_migration):
    """The function who will create the creators and subscribers groups
       the create_groups function assigns existing users to the appropriate groups during migration"""

    # ensure that permissions have been created
    emit_post_migrate_signal(verbosity=1, interactive=False, db='default')

    # Retrieve models using the apps.get_model() function
    # we cannot access models directly from imports, use the apps.get_model() function to retrieve them
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Each model created in Django has four permissions which are generated in parallel.
    # Get permissions for Photo model
    add_photo = Permission.objects.get(codename='add_photo')
    change_photo = Permission.objects.get(codename='change_photo')
    delete_photo = Permission.objects.get(codename='delete_photo')
    view_photo = Permission.objects.get(codename='view_photo')

    creator_permissions = [add_photo, change_photo, delete_photo, view_photo]

    # Create the creators group
    creators = Group(name='creators')
    creators.save()
    # Assign permissions to the creators groups
    creators.permissions.set(creator_permissions)
    # The set() function on a field of type ManyToManyField expects a list of objects
    # The set method replaces all current permissions in the group with the specified ones

    # Create the subscribers groups
    subscribers = Group(name='subscribers')
    subscribers.save()
    # Assign permissions to the subscribers groups
    subscribers.permissions.add(view_photo)
    # The add() method on a ManyToManyField does not take a list as an argument, but the individual objects
    # The add method would add permissions to those already present

    # Assign existing users to the appropriate groups during migration
    users = User.objects.all()
    for user in users:
        if user.role == 'CREATOR':
            # assign existing users in the database with the Group.user_set.add() function
            creators.user_set.add(user)
        if user.role == 'SUBSCRIBER':
            # assign existing users in the database with the Group.user_set.add() function
            subscribers.user_set.add(user)


class Migration(migrations.Migration):
    # list the migrations that must be executed before this one
    dependencies = [
        ("authentication", "0002_alter_user_profile_photo_alter_user_role"),
    ]
    # list of operations that the migration will perform
    operations = [
        # add the create_groups function as an argument to the migrations.RunPython class
        migrations.RunPython(create_groups)
    ]
