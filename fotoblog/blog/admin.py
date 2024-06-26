from django.contrib import admin

# Register your models here
from .models import Blog, Photo


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'uploader', 'date_created')
    list_filter = ("date_created",)


class BlogAdmin(admin.ModelAdmin):
    # list_display = ('title', 'photo', 'content', 'author', 'date_created', 'starred', 'word_count')
    list_display = ('title', 'photo', 'content', 'date_created', 'starred', 'word_count')
    search_fields = ['title', 'content']
    list_editable = ("starred",)
    # prepopulated_fields = {'slug': ('title',)}

    # ManyToManyField dans la liste list_display
    # def display_contributors(self, obj):
    #     return ", ".join(contributor for contributor in obj.contributors.all())
    # display_contributors.short_description = 'Contributors'


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Blog, BlogAdmin)

