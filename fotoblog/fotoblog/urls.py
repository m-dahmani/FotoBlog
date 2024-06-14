"""
URL configuration for fotoblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
# from authentication import views
import authentication.views
import blog.views

urlpatterns = [
    # path('', authentication.views.LoginPageView.as_view(), name='login'),  # To be a class-based view with forms.py
    # path('home/', blog.views.HomePageView.as_view(), name='home'), # To be a class-based view with forms.py
    # path('signup/', authentication.views.SignupView.as_view(), name='signup'),  # To be a class-based view

    # path('', LoginView.as_view(
    #     template_name='authentication/login.html',
    #     redirect_authenticated_user=True),
    #      name='login'), # Implement login with generic views (class LoginView)

    # path('logout/', LogoutView.as_view(
    #     template_name='authentication/login.html'),
    #      name='logout'),  # Implement login with generic views (class LogoutView)

    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),  # the function-based connection view
    path('home/', blog.views.home, name='home'),
    path('photo/upload/', blog.views.photo_upload, name='photo-upload'),
    path('blog/add/', blog.views.blog_and_photo_upload, name='blog-create'),
    path('blog/<int:blog_id>/', blog.views.blog_view_detail, name='blog-view-detail'),


    path('profile/upload/', authentication.views.upload_profile_photo, name='profile-upload'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path("password_change/", PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name="password_change"),

    path("password_change/done/", PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name="password_change_done",),
]


# Configuration is used to serve media files in development(DEBUG=1) (like images uploaded by users)
# In production(DEBUG=0), configure a web server like Nginx or Apache to manage media files.
# or to another host a third-party service
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
