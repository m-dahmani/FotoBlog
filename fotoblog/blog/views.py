from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoForm, BlogForm, DeleteBlogForm, FollowUsersForm
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
    # Take a look at « request.user»  »
    user = request.user
    print(user.get_all_permissions())  # Return the user permissions
    print(user.has_perm('blog.add_photo'))  # Return True for the creators False for the subscribers
    print(user.has_perm('blog.add_blog'))   # Return True for the creators False for the subscribers

    photos = Photo.objects.all()  # recover photos that have been loaded
    blogs = Blog.objects.all()  # recover the instances(Blog) in the home page
    return render(request, 'blog/home.html', {'photos': photos, 'blogs': blogs})


@login_required  # Restrict access to the user connected
@permission_required('blog.add_photo', raise_exception=True)  # to limit access based on permission
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
@permission_required(['blog.add_photo', 'blog.add_blog'], raise_exception=True)  # to limit access based on permission
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
            # blog.author = request.user  # assign a user connected to the author : put the user connected
            blog.photo = photo  # assign a photo to the photo field : fill the photo field to object Blog
            blog.save()  # # save the blog in the DB
            # store the relationships in the ManyToManyField after the model has been saved
            # add the user connected as a contributor once the blog instance is saved
            # use the add method to create the ManyToMany relationship
            # specify the contents of additional fields with the argument through_defaults
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
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


@login_required
@permission_required(['blog.change_blog', 'change_blog_title'], raise_exception=True)
def edit_delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':
        # check which form is sent by checking the presence of this field (edit_blog) in the POST data
        if 'edit_blog' in request.POST:
            # we pre-fill the form with an existing blog the instance already created and fill it with the POST data
            edit_form = BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                # update the instance of the object already created “Blog” and save it in the database
                edit_form.save()
                # return redirect('home')
                # redirect to the detail page of the blog we just update
                return redirect('blog-view-detail', blog.id)

        # check which form is sent by checking the presence of this field (delete_blog) in the POST data
        if 'delete_blog' in request.POST:

            if 'confirm' in request.POST:
                # Create an instance of our form and fill it with the POST data
                delete_form = DeleteBlogForm(request.POST)  # ??? no need this

                if delete_form.is_valid():  # ??? no need this
                    # delete the blog object in the database
                    blog.delete()
                    # redirect to the list-page of the blog we just verified if existing it
                    return redirect('home')

            elif 'cancel' in request.POST:
                # redirect to the list-page of the blog we just verified if existing it
                return redirect('home')
    else:
        # we pre-fill the form with an existing blog the instance already created
        # this must be a GET request, so open with the instance of the object already created
        edit_form = BlogForm(instance=blog)
        # this must be a GET request, so create an empty form
        delete_form = DeleteBlogForm()  # Add a new DeleteBlogForm empty here if request.GET

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_delete_blog.html', context)


# # just to delete photos via home interface
# @login_required
# def delete_photo(request, photo_id):
#     photo = get_object_or_404(Photo, id=photo_id)
#
#     # Take a look at « request.method » and « request.POST »
#     print('La méthode de requête est : ', request.method)
#     print('Les données POST sont : ', request.POST)
#     print('Les données login : ', request.user)
#     print('Les données Media : ', request.FILES)
#
#     if request.method == 'POST':
#         if 'confirm' in request.POST:
#             # delete the photo object in the database
#             photo.delete()
#             # redirect to the list-page of the blog we just verified if existing it
#             return redirect('home')
#
#         elif 'cancel' in request.POST:
#             # redirect to the list-page of the photo we just verified if existing it
#             return redirect('home')
#
#     context = {'photo': photo}
#     return render(request, 'blog/delete_photo.html', context)
#
#
# @login_required
# def photo_view_detail(request, photo_id):
#     # to recover the blog(obj) and handle the case where the object does not exist.
#     photo = get_object_or_404(Photo, id=photo_id)
#     context = {'photo': photo}
#     return render(request, 'blog/photo_view_detail.html', context)
# ####################################################################


@login_required
@permission_required('blog.add_photo', raise_exception=True)  # to limit access based on permission
def create_multiple_photos(request):  # create a view that allows you to upload multiple photos at once
    # use the formset_factory method to create and generate a class that will be our FormSet
    PhotoFormSet = formset_factory(PhotoForm, extra=5)  # extra=5 == the number of instances
    formset = PhotoFormSet()  # we instantiate the class

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':

        formset = PhotoFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:  # iterate through each form in Formset
                # for each Formset form, we will check if there is data in it
                # (because even if the form is valid, one or more forms are empty, they must be ignored)
                if form.cleaned_data:  # This allows you to check the current form, we have data that is not empty
                    # and in this case, we can manage it
                    photo = form.save(commit=False)
                    photo.uploader = request.user  # assign the uploader field to the request user
                    photo.save()  # we will save the photo

            return redirect('home')  # outside the loop we will return the redirection to the home page

    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})


@login_required
def follow_users(request):

    # Take a look at « request.user»  »
    print('Les données login : ', request.user)
    user = request.user
    print(user.get_all_permissions())  # Return the user permissions
    print(user.has_perm('blog.add_photo'))  # Return True for the creators False for the subscribers
    print(user.has_perm('blog.add_blog'))  # Return True for the creators False for the subscribers

    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)

    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FollowUsersForm(instance=request.user)
    return render(request, 'blog/follow_users_form.html', context={'form': form})