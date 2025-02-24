from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'gymapp/index.html')
def about_view(request):
    return render(request, 'gymapp/about.html')

