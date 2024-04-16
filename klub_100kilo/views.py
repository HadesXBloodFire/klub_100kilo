from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from klub_100kilo.models import Reservations, Users
from django.contrib.auth import authenticate, login, get_user_model, login as auth_login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password



@login_required
def main_page(request):
    return render(request, 'main.html')


def hero_page(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'hero.html')


@login_required
def main_page(request):
    user_reservations = Reservations.objects.filter(user_id=1, date__gt=timezone.now())
    for reservation in user_reservations:
        reservation.trainer = Users.objects.get(user_id=reservation.trainer_id)
    return render(request, 'main.html', {'reservations': user_reservations})


def reservation_view(request):
    return render(request, 'reservation_main_page.html')


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})
#
#
# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = get_user_model().objects.filter(email=email).first()
#             if user is not None and user.check_password(password):
#                 login(request, user)
#                 return redirect('main_page')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Tworzymy instancję naszego własnego modelu Users
            user = Users()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.mail = form.cleaned_data.get('email')
            user.password = make_password(form.cleaned_data.get('password'))  # Hashujemy hasło przed zapisaniem go
            user.role = 'User'
            user.save()  # Zapisz użytkownika do bazy danych

            django_user = get_user_model().objects.create_user(
                username=form.cleaned_data.get('email'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
            )
            django_user.save()

            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})