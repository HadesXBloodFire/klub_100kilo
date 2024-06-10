import os

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from klub_100kilo.models import *
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
    login as auth_login,
)

from .forms import RegisterForm, LoginForm, EditProfileForm, GoalForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.views.decorators.http import require_GET
from .serializers import ReservationSerializer


def get_user(request):
    logged_in_user = get_user_model().objects.get(email=request.user.email)
    return Users.objects.get(mail=logged_in_user.email)


def hero_page(request):
    if request.user.is_authenticated:
        return redirect("main_page")
    return render(request, "hero.html")


@login_required
def main_page(request):
    user_reservations = Reservations.objects.filter(
        user_id=get_user(request).user_id, start__gt=timezone.now()
    )
    for reservation in user_reservations:
        reservation.trainer = Users.objects.get(user_id=reservation.trainer_id)
    return render(request, "main.html", {"reservations": user_reservations})


def reservation_view(request):
    return render(request, "reservation_main_page.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "User with this email already exists.")
                return render(request, "register.html", {"form": form})
            user = Users()
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.phone_number = form.cleaned_data.get("phone_number")
            user.mail = email
            user.password = make_password(form.cleaned_data.get("password"))
            user.role = "User"
            user.save()

            django_user = get_user_model().objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data.get("password"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
            )
            django_user.save()

            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
def account(request):
    return render(request, "account.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("main_page")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})


def book_trainer(request):
    if request.method == "POST":
        # Tutaj dodajemy logikę przypisywania trenera do rezerwacji
        pass
    else:
        reservations = Reservations.objects.filter(user=get_user(request))
        trainers = Trainers.objects.select_related(
            "user"
        ).all()  # Pobieramy wszystkich trenerów i ich powiązane dane użytkownika
        return render(
            request,
            "book_trainer.html",
            {"reservations": reservations, "trainers": trainers},
        )


def logout_view(request):
    logout(request)
    return redirect("hero_page")


@require_GET
def get_measurements(request, year, month, day):
    date = timezone.datetime(year, month, day).date()
    user = get_user(request)
    measurements = (
        Measurements.objects.filter(user=user, date__lte=date)
        .order_by("-date")
        .first()
    )
    if measurements:
        data = {
            "weight": measurements.weight,
            "biceps_size": measurements.biceps_size,
            "bust_size": measurements.bust_size,
            "waist_size": measurements.waist_size,
            "thighs_size": measurements.thighs_size,
            "height": measurements.height,
        }
    else:
        data = {}
    return JsonResponse(data)


@csrf_exempt
@login_required
def post_measurements(request, year, month, day):
    if request.method == "POST":
        data = json.loads(request.body)
        user = get_user(request)
        date = timezone.datetime(year, month, day).date()
        measurement = Measurements.objects.filter(user=user, date=date).first()
        if measurement is None:
            measurement = Measurements(user=user, date=date)
        measurement.height = data.get("height")
        measurement.weight = data.get("weight")
        measurement.bust_size = data.get("chest_circumference")
        measurement.biceps_size = data.get("biceps_size")
        measurement.waist_size = data.get("waist_size")
        measurement.thighs_size = data.get("thighs_size")
        measurement.save()
        update_goals_status(user)
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"},
            status=400,
        )


@csrf_exempt
@login_required
def measurements_view(request):
    user = get_user(request)
    measurements = Measurements.objects.filter(user=user).order_by("-date")
    today = timezone.now().date()
    today_measurement = measurements.filter(date=today).first()
    return render(
        request,
        "measurements.html",
        {"measurements": measurements, "today_measurement": today_measurement},
    )



@require_GET
def get_diets(request, year, month, day):
    date = timezone.datetime(year, month, day).date()
    user = get_user(request)
    diets = Diet.objects.filter(user=user, date__lte=date).order_by('-date').first()
    if diets:
        data = {
            'meal': diets.meal,
            'description': diets.description,
            'calories': diets.calories,
        }
    else:
        data = {}
    return JsonResponse(data)


@csrf_exempt
@login_required
def post_diets(request, year, month, day):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_user(request)
        date = timezone.datetime(year, month, day).date()
        diet = Diet.objects.filter(user=user, date=date).first()
        if diet is None:
            diet = Diet(user=user, date=date)
        diet.meal = data.get('meal')
        diet.description = data.get('description')
        diet.calories = data.get('calories')
        diet.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def diet_view(request):
    user = get_user(request)
    diets = Diet.objects.filter(user=user).order_by('-date')
    today = timezone.now().date()
    today_diet = diets.filter(date=today).first()
    return render(request, 'diet.html', {'diets': diets, 'today_diet': today_diet})

@login_required
@csrf_exempt
def book_training(request):
    if request.method == "POST":
        start_time = request.POST.get("start")
        end_time = request.POST.get("end")
        user_id = request.user.id

        reservation = Reservation(
            start_time=start_time, end_time=end_time, user_id=user_id
        )
        reservation.save()

        return JsonResponse({"message": "Reservation created successfully."})
    else:
        return render(request, "book_training.html")


@api_view(["GET"])
def get_reservations(request):
    reservations = Reservations.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_reservation(request):
    start_time = request.data.get("start")
    end_time = request.data.get("end")

    logged_in_user = get_user_model().objects.get(email=request.user.email)
    user = Users.objects.get(mail=logged_in_user.email)

    reservation = Reservations(
        user=user,
        type="Training",
        status="P",
        date=timezone.now(),
        start_time=start_time,
        end_time=end_time,
    )

    reservation.save()

    return Response({"message": "Reservation created successfully."})

@csrf_exempt
@login_required
def goals_view(request):
    user = get_user(request)
    goals = MeasurementsGoals.objects.filter(user=user)
    achieved_goals = goals.filter(status='Z').count()
    total_goals = goals.count()
    percentage = (achieved_goals / total_goals) * 100 if total_goals > 0 else 0
    return render(request, 'goals.html', {'goals': goals, 'percentage': percentage})

@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = get_user(request)
            goal.save()
            return redirect('goals')
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = GoalForm()
    return render(request, 'add_goal.html', {'form': form})


def update_goals_status(user):
    goals = MeasurementsGoals.objects.filter(user=user)
    measurements = Measurements.objects.filter(user=user).order_by('-date').first()

    if measurements is None:
        return

    for goal in goals:
        if goal.status == 'Z':
            continue

        if goal.start_date <= measurements.date <= (goal.start_date + timedelta(days=goal.max_days)):
            conditions = [
                (goal.weight is None or measurements.weight <= goal.weight),
                (goal.biceps_size is None or measurements.biceps_size >= goal.biceps_size),
                (goal.bust_size is None or measurements.bust_size >= goal.bust_size),
                (goal.waist_size is None or measurements.waist_size >= goal.waist_size),
                (goal.thighs_size is None or measurements.thighs_size >= goal.thighs_size),
                (goal.height is None or measurements.height >= goal.height)
            ]
            if all(conditions):
                goal.status = 'Z'
                goal.save()

@login_required
def workouts_view(request):
    trainings = Trainings.objects.filter(user=get_user(request))
    exercises = Exercises.objects.all()
    return render(request, 'workouts.html', {'trainings': trainings, 'exercises': exercises})

@require_POST
@login_required
def create_training(request):
    print(request.POST)
    name = request.POST.get('name')
    exercise_ids = request.POST.getlist('exercises')
    exercise_ids = list(filter(None, exercise_ids))
    if not exercise_ids:
        messages.error(request, "No exercises selected.")
        return redirect('workouts')
    exercises = Exercises.objects.filter(exercise_id__in=exercise_ids)
    if len(exercises) != len(exercise_ids):
        messages.error(request, "Some exercises could not be found.")
        return redirect('workouts')
    training = Trainings(name=name, user=get_user(request))
    training.save()
    for exercise in exercises:
        training_exercise = TraningsExercises(training=training, exercise=exercise)
        training_exercise.save()
    return redirect('workouts')

@require_POST
@login_required
def mark_exercises_as_succeeded(request, training_id):
    checked_exercise_ids = request.POST.getlist('exercises')
    checked_exercise_ids = list(filter(None, checked_exercise_ids))
    all_exercise_ids = [str(te.exercise.exercise_id) for te in TraningsExercises.objects.filter(training_id=training_id)]
    unchecked_exercise_ids = list(set(all_exercise_ids) - set(checked_exercise_ids))
    TraningsExercises.objects.filter(training_id=training_id, exercise_id__in=unchecked_exercise_ids).update(succeded=False)
    TraningsExercises.objects.filter(training_id=training_id, exercise_id__in=checked_exercise_ids).update(succeded=True)
    return redirect('workouts')