from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Membership,Member, Attendance
from .forms import UserDetailForm
from .models import Member
from .forms import UserDetailForm
from datetime import datetime


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

def services_view(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        attendance_ids = request.POST.getlist('attendance')
        for member_id in attendance_ids:
            member = Member.objects.get(id=member_id)
            Attendance.objects.create(member=member, date=selected_date)
        return HttpResponse("Attendance marked successfully!")

    members = Member.objects.all()
    return render(request, 'gymapp/services.html', {'Members': members})