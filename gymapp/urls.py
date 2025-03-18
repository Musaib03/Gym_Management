from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('about', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),  # Services route
    path('membership-form/', views.membership_form, name='membership_form'),
    path('membership-success/', views.membership_success, name='membership_success'),
    path('track', views.track, name='track'),
    path('workout-plan/', views.workout_plan_view, name='workout_plan'),
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
