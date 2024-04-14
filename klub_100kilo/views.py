from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def main_page(request):
    return render(request, 'main.html')


def hero_page(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'hero.html')


@login_required
def main_page(request):
    return render(request, 'main.html')


def reservation_view(request):
    return render(request, 'reservation_main_page.html')