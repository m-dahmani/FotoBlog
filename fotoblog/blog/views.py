from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoForm, BlogForm
from .models import Photo, Blog


# Restrict access to the home page => with class HomePageView(LoginRequiredMixin, TemplateView)
# class HomePageView(LoginRequiredMixin, TemplateView):
#     """Refactor the login view to be a class-based view"""
#     template_name = 'blog/home.html'
#     # URL where non-authenticated users will be redirected and by default setting.LOGIN_URL = 'login'
#     login_url = ''
#     redirect_field_name = 'redirect_to'  # Field for redirecting users after login


# the function-based connection view
@login_required  # Restrict access to the home page and by default setting.LOGIN_URL = 'login'
def home(request):
    photos = Photo.objects.all()  # recover photos that have been loaded
    blogs = Blog.objects.all()  # recover the instances(Blog) in the home page
    return render(request, 'blog/home.html', {'photos': photos, 'blogs': blogs})


@login_required  # Restrict access to the user connected
def photo_upload(request):
    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)  # pass data & images(FILES) to form
        if form.is_valid():
            photo = form.save(commit=False)  # to not save the object in the database with commit=False
            # Initialize & set the uploader to the user connected before saving the model
            photo.uploader = request.user  # assign a value to the uploader field: we will put the user connected
            # now we can save
            photo.save()  # save the photo in the DB
            return redirect('home')

    else:
        form = PhotoForm()  # get the PhotoForm()

    return render(request, 'blog/photo_upload.html', context={'form': form})  # to pass it to the template


@login_required  # Restrict access to the user connected
def blog_and_photo_upload(request):
    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':

        blog_form = BlogForm(request.POST)  # pass data to form
        photo_form = PhotoForm(request.POST, request.FILES)  # pass data & images(FILES) to form

        if any([blog_form.is_valid(), photo_form.is_valid()]):

            photo = photo_form.save(commit=False)  # to not save the object in the database with commit=False
            photo.uploader = request.user  # assign a user connected to the uploader : put the user connected
            photo.save()  # save the photo in the DB

            blog = blog_form.save(commit=False)  # to not save the object in the database with commit=False
            blog.author = request.user  # assign a user connected to the author : put the user connected
            blog.photo = photo  # assign a photo to the photo field : fill the photo field to object Blog
            blog.save()  # save the blog in the DB

            return redirect('home')

    else:
        blog_form = BlogForm()  # get the PhotoForm()
        photo_form = PhotoForm()  # get the PhotoForm()

    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/blog_post_create.html', context=context)  # to pass it to the template


@login_required
def blog_view_detail(request, blog_id):
    # to recover the blog(obj) and handle the case where the object does not exist.
    blog = get_object_or_404(Blog, id=blog_id)
    context = {'blog': blog}
    return render(request, 'blog/blog_view_detail.html', context)
