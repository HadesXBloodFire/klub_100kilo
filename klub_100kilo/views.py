import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from klub_100kilo.models import Reservations, Users, Trainers
from django.contrib.auth import authenticate, login, get_user_model, login as auth_login
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages


def get_user(request):
    logged_in_user = get_user_model().objects.get(email=request.user.email)
    return Users.objects.get(mail=logged_in_user.email)

  
@login_required
def main_page(request):
    return render(request, "main.html")


def hero_page(request):
    if request.user.is_authenticated:
        return redirect("main_page")
    return render(request, "hero.html")


@login_required
def main_page(request):
    user_reservations = Reservations.objects.filter(user_id=get_user(request).user_id, date__gt=timezone.now())
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
    return render(request, 'account.html')


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
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def book_trainer(request):
    if request.method == 'POST':
        # Tutaj dodajemy logikę przypisywania trenera do rezerwacji
        pass
    else:
        reservations = Reservations.objects.filter(user=get_user(request))
        trainers = Trainers.objects.select_related('user').all()  # Pobieramy wszystkich trenerów i ich powiązane dane użytkownika
        return render(request, 'book_trainer.html', {'reservations': reservations, 'trainers': trainers})
def book_training(request):
    return render(request, 'book_training.html')

def logout_view(request):
    logout(request)
    return redirect("hero_page")


def diet_view(request):
    with open('nictakiego.txt', 'r') as file:
        github_token = file.read().strip()

    context = {
        'user_id': get_user(request).user_id,
        'github_token': github_token
    }
    return render(request, 'diet.html', context)

