from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Membership
from .forms import UserDetailForm
from .models import Member
from .forms import UserDetailForm

def home_view(request):
    return render(request, 'gymapp/index.html')
def about_view(request):
    return render(request, 'gymapp/about.html')
# Membership Form View
def membership_form(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('membership_success')
    else:
        form = UserDetailForm()
    return render(request, 'gymapp/membership_form.html', {'form': form})

# Success View
def membership_success(request):
    return HttpResponse("<h1>Membership successfully registered!</h1>")