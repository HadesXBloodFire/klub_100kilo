import os
import datetime


from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from klub_100kilo.models import Reservations, Users, Trainers, Measurements, Diet, Events
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
    login as auth_login,
)

from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.views.decorators.http import require_GET


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
        try:
            reservation.trainer = Users.objects.get(user_id=reservation.trainer_id)
        except Users.DoesNotExist:
            reservation.trainer = None
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
        selected_trainer_id = int(request.POST.get('trainer'))
        selected_reservation_id = request.POST.get('reservation')

        print(selected_trainer_id)
        print(selected_reservation_id)
        print(type(selected_trainer_id))
        print(type(selected_reservation_id))


        reservation = Reservations.objects.get(reservation_id=selected_reservation_id)

        reservation.trainer_id = selected_trainer_id
        reservation.save()

        return redirect('book_trainer')

    else:
        reservations = Reservations.objects.filter(user=get_user(request))
        trainers = Trainers.objects.select_related("user").all()
        return render(request, "book_trainer.html", {"reservations": reservations, "trainers": trainers})


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


@api_view(["GET"])
def get_reservations(request):
    reservations = Reservations.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@login_required
@csrf_exempt
def book_training(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'book_training.html', context)


def all_events(request):
    all_events = Reservations.objects.filter(user_id=get_user(request).user_id)
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.reservation_id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })

    return JsonResponse(out, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    user_id = get_user(request).user_id
    event = Reservations(name=str(title), start=start, end=end, user_id=user_id, gym_id=1, status='P', type='Training')
    event.save()
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Reservations.objects.get(reservation_id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Reservations.objects.get(reservation_id=id)
    event.delete()
    data = {}
    return JsonResponse(data)