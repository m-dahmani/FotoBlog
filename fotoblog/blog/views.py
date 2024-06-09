from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Restrict access to the home page => with class HomePageView(LoginRequiredMixin, TemplateView)
class HomePageView(LoginRequiredMixin, TemplateView):
    """Refactor the login view to be a class-based view"""
    template_name = 'blog/home.html'
    # URL where non-authenticated users will be redirected and by default setting.LOGIN_URL = 'login'
    login_url = ''
    redirect_field_name = 'redirect_to'  # Field for redirecting users after login


# @login_required(login_url='') # to pass login_url here or and by default setting.LOGIN_URL = 'login'
# @login_required  # Restrict access to the home page
# def home(request):
#    """the function-based connection view"""
#     return render(request, 'blog/home.html')


