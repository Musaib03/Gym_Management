from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Membership,Member, Attendance
from .forms import UserDetailForm
from .models import Member
from .forms import UserDetailForm
from datetime import datetime

# import tensorflow as tf
# import tensorflow_hub as hub
# import numpy as np
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.core.files.storage import FileSystemStorage
# from tensorflow.keras.preprocessing import image
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'gymapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'gymapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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
        return JsonResponse({"message": "Attendance marked successfully!"})

    members = Member.objects.all()
    return render(request, 'gymapp/services.html', {'Members': members})



import time
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.preprocessing import image
import tensorflow_hub as hub

# Load the TensorFlow Hub model
MODEL_URL = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/5"
model_layer = hub.KerasLayer(MODEL_URL, input_shape=(224, 224, 3), trainable=False)
def simulate_body_structure(predicted_label):
    # Simulate body structure based on predicted label
    simulated_categories = ['lean', 'muscular', 'overweight']
    return simulated_categories[predicted_label % len(simulated_categories)]

def track(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        uploaded_image = request.FILES.get('image')

        if not (name and age and weight and uploaded_image):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        # Save the image temporarily
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        full_image_path = fs.path(image_path)

        # Preprocess the image
        img = image.load_img(full_image_path, target_size=(224, 224))  # Ensure correct input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Predict using the model layer
        try:
            predictions = model_layer(img_array).numpy()  # Use the KerasLayer directly
            predicted_label = np.argmax(predictions)
            body_structure = simulate_body_structure(predicted_label)
        except Exception as e:
            return JsonResponse({'error': f'Error during prediction: {str(e)}'}, status=500)

        # Simulate processing delay
        time.sleep(2)  # Add a 2-second delay

        # Generate workout and diet plans based on predicted_label
        # Map ImageNet predictions to custom categories
        label_to_category = {
            0: 'lean',    
            1: 'muscular', 
            2: 'overweight', 
        }

        # Function to map predicted label to category
        def map_label_to_category(label):
            return label_to_category.get(label, 'default')
        # Default fallback if no category matches

        # Generate insights based on category
        category = map_label_to_category(predicted_label)
        if category is None:
            category = 'default'  # Fallback category

        workout_and_diet = {
            0: {
                'workout': [
                    f"{name}, focus on strength training exercises like squats, deadlifts, and bench press.",
                    "Incorporate HIIT sessions twice a week.",
                    "Add core strengthening exercises like planks and leg raises."
                ],
                'diet': [
                    "High-protein meals: chicken, fish, tofu, and legumes.",
                    "Include complex carbs: brown rice, quinoa, and sweet potatoes.",
                    "Stay hydrated with at least 3 liters of water daily."
                ],
            },
            1: {
                'workout': [
                    f"{name}, focus on endurance exercises like jogging, cycling, and swimming.",
                    "Add yoga or pilates for improved flexibility and mental relaxation.",
                    "Include light strength training to maintain muscle tone."
                ],
                'diet': [
                    "Balanced meals with an emphasis on vegetables, fruits, and lean protein.",
                    "Limit sugar and processed foods.",
                    "Drink herbal teas and include healthy fats like avocado and nuts."
                ],
            },
            2: {
                'workout': [
                    f"{name}, try functional fitness workouts like kettlebell swings and burpees.",
                    "Mix in outdoor activities such as hiking or playing sports.",
                    "Focus on mobility exercises to prevent injuries."
                ],
                'diet': [
                    "Low-fat meals with a focus on high-fiber foods like oatmeal and salads.",
                    "Include lean protein sources like eggs and chicken.",
                    "Avoid junk food and sugary beverages."
                ],
            },
            'default': {
                'workout': [
                    f"{name}, try functional fitness workouts like kettlebell swings and burpees..",
                    "Incorporate light aerobic exercises to stay healthy."
                    "Stay hydrated with at least 3 liters of water daily."
                ],
                'diet': [
                    "A balanced diet with all macros in proper proportion.",
                    "Limit sugar and processed foods."
                    "High-protein meals: chicken, fish, tofu, and legumes"
                ],
            },
        }

        insights = workout_and_diet.get(category, workout_and_diet['default'])


        # Randomly pick one suggestion from each list to vary responses
        workout_plan = np.random.choice(insights['workout'])
        diet_plan = np.random.choice(insights['diet'])

        return JsonResponse({
            'name': name,
            'age': age,
            'weight': weight,
            'workout_plan': workout_plan,
            'diet_plan': diet_plan,
        })

    return render(request, 'gymapp/tracker.html')

def workout_plan_view(request):
    if request.method == 'POST':
        level = request.POST.get('level')  # Get the selected level from the form

        # Define workout and diet plans for each level
        plans = {
            'beginner': {
                'workout': [
                    {'day': 'Day 1', 'activity': 'Full-body stretching', 'image': 'https://www.himalayanyogaashram.com/wp-content/uploads/2021/09/Why-Stretching-Daily-Is-The-Key-To-Your-Fitness-Benefits-of-Full-Body-Stretches.jpg'},
                    {'day': 'Day 2', 'activity': 'Cardio: 20 minutes jogging', 'image': 'https://img.freepik.com/free-photo/young-bodybuilder-running-cardio-workout-looking-gym-window_496169-2718.jpg'},
                    {'day': 'Day 3', 'activity': 'Rest day', 'image': 'https://jooinn.com/images/relaxation-3.jpg'},
                    {'day': 'Day 4', 'activity': 'Bodyweight exercises', 'image': 'https://www.offgridweb.com/wp-content/uploads/2015/10/Body-Weight-Exercises-thumbnail.jpg'},
                    {'day': 'Day 5', 'activity': 'Cardio: 15 minutes cycling', 'image': 'https://i.pinimg.com/originals/74/97/3a/74973a64e97d15605ee0909eabd80758.jpg'},
                    {'day': 'Day 6', 'activity': 'Yoga session', 'image': 'https://yogaashfield.com.au/wp-content/uploads/2020/02/yoga-for-men2.jpg'},
                ],
                'diet': ['Breakfast: Oatmeal', 'Lunch: Grilled chicken salad', 'Dinner: Steamed vegetables']
            },
            'intermediate': {
                'workout': [
                    {'day': 'Day 1', 'activity': 'Strength training: Upper body', 'image': 'https://builtwithscience.com/wp-content/uploads/2018/03/upper-body-workout-thumbnail.png'},
                    {'day': 'Day 2', 'activity': 'Cardio: 30 minutes running', 'image': 'https://images.saymedia-content.com/.image/t_share/MTc1MTI3NzM2MjkyMDI1NDM5/the-different-types-of-cardio-and-their-benefits.jpg'},
                    {'day': 'Day 3', 'activity': 'Lower body workout', 'image': 'https://th.bing.com/th/id/OIP.h0XpZGlsZsaqG-vNhE14_wHaD4?rs=1&pid=ImgDetMain'},
                    {'day': 'Day 4', 'activity': 'HIIT session', 'image': 'https://th.bing.com/th/id/OIP.9tG-0CAnFHasAplBWY6biAHaGI?rs=1&pid=ImgDetMain'},
                    {'day': 'Day 5', 'activity': 'Core workout', 'image': 'https://darebee.com/images/workouts/total-core-workout.jpg'},
                    {'day': 'Day 6', 'activity': 'Yoga and recovery', 'image': 'https://centerforliving.org/wp-content/uploads/2023/09/blog-yoga-for-recovery.jpg'},
                ],
                'diet': ['Breakfast: Protein smoothie', 'Lunch: Quinoa and grilled fish', 'Dinner: Salad with nuts']
            },
            'advanced': {
                'workout': [
                    {'day': 'Day 1', 'activity': 'Weightlifting: Chest and arms', 'image': 'https://c.wallhere.com/photos/49/9c/men_bodybuilding_weightlifting_sport-53362.jpg!d'},
                    {'day': 'Day 2', 'activity': 'CrossFit session', 'image': 'https://i.ytimg.com/vi/QBah01ovrWQ/maxresdefault.jpg'},
                    {'day': 'Day 3', 'activity': 'Leg day', 'image': 'https://th.bing.com/th/id/OIP.e5QKnDgmhACvvMbl4o4ohQAAAA?rs=1&pid=ImgDetMain'},
                    {'day': 'Day 4', 'activity': 'Endurance training', 'image': 'https://www.runladylike.com/wp-content/uploads/2014/01/5-Phases-of-training.jpg'},
                    {'day': 'Day 5', 'activity': 'Powerlifting', 'image': 'https://wallpaperaccess.com/full/2803801.jpg'},
                    {'day': 'Day 6', 'activity': 'Active recovery', 'image': 'https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/11/Active_recovery_GettyImages1265162147_Header-1024x575.jpg'},
                ],
                'diet': ['Breakfast: Eggs and avocado', 'Lunch: Lean beef with veggies', 'Dinner: Grilled salmon']
            }
        }

        selected_plan = plans.get(level, {})
        return render(request, 'gymapp/workout_plan.html', {'level': level, 'plan': selected_plan})

    return render(request, 'gymapp/workout_plan.html')

