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
            predicted_label = np.argmax(predictions)  # Get the index of the highest probability
        except Exception as e:
            return JsonResponse({'error': f'Error during prediction: {str(e)}'}, status=500)

        # Simulate processing delay
        time.sleep(2)  # Add a 2-second delay

        # Generate workout and diet plans based on predicted_label
        # Map ImageNet predictions to custom categories
        label_to_category = {
            range(0, 100): 0,   # Example mapping: ImageNet classes 0-99 → Category 0
            range(100, 200): 1, # Example mapping: ImageNet classes 100-199 → Category 1
            range(200, 300): 2, # Example mapping: ImageNet classes 200-299 → Category 2
            # Add more mappings as needed
        }

        # Function to map predicted label to category
        def map_label_to_category(label):
            for label_range, category in label_to_category.items():
                if label in label_range:
                    return category
            return None  # Default fallback if no category matches

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
