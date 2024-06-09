from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



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
    return render(request, 'blog/home.html')


