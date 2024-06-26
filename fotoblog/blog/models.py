from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Photo(models.Model):
    image = models.ImageField()  # The Photo template contains an image stored in the ImageField.
    caption = models.CharField(max_length=128, blank=True)
    # Adds an uploader field as a foreign key to the user.
    # Use settings.AUTH_USER_MODEL to reference the custom user model if necessary.
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):

        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # saving the resized image to the file system
        # this is not the save() method of the model Photo !
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        Because if the specifications change, and the template method starts taking new and different arguments,
        your custom method will be able to handle them, thanks to generic *args and **kwargs.
        and provide them to the super() method
        """
        super().save(*args, **kwargs)
        # Add easily the methode resize_image()
        # to override the save method in order to add the resize_image automatically
        # To do this, we will use the resize_image function to generate Photo.objects.all().resize_image() automatically
        self.resize_image()

    # def __str__(self):
    #     return f'{self.image}'


class Blog(models.Model):
    # blog posts can optionally be linked to a photo using the ForeignKey relationship
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    # slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.CharField(max_length=5000)
    # remove the author field from Blog we will have several contributors
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # remove after migration
    date_created = models.DateTimeField(auto_now_add=True)
    # last_updated = models.DateTimeField(auto_now=True)
    # published = models.BooleanField(default=False, verbose_name="Publié")
    starred = models.BooleanField(default=False)
    # Create a new word_count field on the Blog model. You can set null=True to avoid having to provide a default value.
    word_count = models.fields.IntegerField(null=True, blank=True)

    # Authorize a Blog model instead of having a single author we will have several contributors
    # Add & Update a M2M to Blog and tell it to use the intermediate table via through
    # access all Blog instances having the User as a contributor using user.contributions instead
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor',
                                          related_name='contributions')

    def _get_word_count(self):
        """Add a new _get_word_count() method to the Blog model,
         which calculates the number of words in the content field. """
        return len(self.content.split())

    def save(self, *args, **kwargs):
        # to override & Update the save method to assign to word_count the result of _get_word_count()
        self.word_count = self._get_word_count()
        # before calling the save() method of the parent class.
        super().save(*args, **kwargs)

    class Meta:
        # Specify custom permissions by configuring the permissions attribute in a Meta class of a model
        permissions = [
            ('change_blog_title', 'Can change the title of a blog post')
        ]

    # We are going to add some information to the model, in particular a Meta class which will allow us
    # to modify the default display order of articles in the administration interface
    # as well as the displayed name (by default, the interface would display the model name, therefore(donc) Blog)
    # We add a Meta class to specify our model
    # class Meta:
    #     ordering = ['-date_created']
        # verbose_name = "Article"

    # def __str__(self):
    #     return self.title

    # def save(self, *args, **kwargs):
    #     """
    # Finally, I like to override the save method in order to add the slug automatically
    # depending on the title of the article.
    # To do this, we will use the slugify function of the module django.template.defaultfilters :
    # """
    # If no slug is indicated by the author of the article, we use slugify on the title of the article
    # # to generate one automatically 😉

    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #
    #     super().save(*args, **kwargs)


# This code uses a post_delete Signal handler to delete the image file when the Photo instance is deleted.
@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)


class BlogContributor(models.Model):
    """The intermediate table requires two ForeignKey to the two models involved in the ManyToMany relationship"""
    # a relationship to the User
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # a relationship to the Blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # to store information about contributions specific to each author
    contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        # to ensure that there is only one BlogContributor instance for each contributor pair
        unique_together = ('contributor', 'blog')









