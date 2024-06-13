from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import Photo


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
    return render(request, 'blog/home.html', {'photos': photos})


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


