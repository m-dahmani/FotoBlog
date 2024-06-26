# Generated by Django 4.2.13 on 2024-06-06 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(upload_to="", verbose_name="Profile picture"),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("CREATOR", "Creator"), ("SUBSCRIBER", "Subscriber")],
                max_length=30,
                verbose_name="Role",
            ),
        ),
    ]
