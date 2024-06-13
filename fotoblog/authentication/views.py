from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, UploadProfilePhotoForm
from django.views.generic import View


# class LoginPageView(View):
#     """Refactor the login view to be a class-based view"""
#     template_name = 'authentication/login.html'
#     form_class = LoginForm
#
#     def get(self, request):
#         message = ''
#         form = self.form_class()
#
#         context = {'form': form, 'message': message}
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         message = ''
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 message = 'Invalid credentials'
#
#         context = {'form': form, 'message': message}
#         return render(request, self.template_name, context)


# the function-based connection view
def login_page(request):
    message = ''  # Initialize 'message' with an empty string or a default value

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)

    if request.method == 'POST':
        # Create an instance of our form and fill it with the POST data
        form = LoginForm(request.POST)
        if form.is_valid():
            # (login code here with authenticate => user or None & login => user connected)
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                # message = f'Hello, {user.username}! You are connected.'
                return redirect('home')  # Redirect to home page
            else:
                message = 'Invalid credentials'
    else:
        # this must be a GET request, so an empty form
        form = LoginForm()  # Initialize the form for GET request

    context = {'form': form, 'message': message}  # pass this form to the template
    return render(request, 'authentication/login.html', context)


# the function-based connection view
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to connexion page


# the function-based connection view
def signup_page(request):

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'authentication/signup.html', context=context)


# class SignupView(View):
#     """Refactor the Signup view to be a class-based view"""
#     form_class = SignupForm
#     template = 'authentication/signup.html'
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#           #  return redirect('home')
#             return redirect(settings.LOGIN_REDIRECT_URL)
#         return render(request, self.template, {'form': form})


@login_required  # Restrict access to the user connected
def upload_profile_photo(request):
    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':
        # pass data & images(FILES) & we pre-fill the form with an existing instance=request.user to form
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  # save the photo in the DB
            return redirect('home')

    else:
        # we pre-fill the form with an existing instance=request.user here if request.GET
        form = UploadProfilePhotoForm(instance=request.user)

    return render(request, 'authentication/photo_profil_upload.html', context={'form': form})
