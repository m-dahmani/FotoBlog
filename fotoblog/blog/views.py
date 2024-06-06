from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required  # Restrict access to the home page
def home(request):
    return render(request, 'blog/home.html')
