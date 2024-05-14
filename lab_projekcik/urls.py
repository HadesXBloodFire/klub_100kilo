"""
URL configuration for lab_projekcik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from klub_100kilo.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reservations/", reservation_view, name="reservations"),
    path("", hero_page, name="hero_page"),
    path("main/", main_page, name="main_page"),
    path("signup/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('account/', account, name='account'),
    path('account/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'),name='change_password'),
    path('account/edit_profile/', edit_profile, name='edit_profile'),
    path('account/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('book_trainer/', book_trainer, name='book_trainer'),
    path('book_training/', book_training, name='book_training'),
    path('diet/', diet_view, name='diet'),
    path('measurements/', measurements_view, name='measurements'),
    path('get_diet_data/<int:year>/<int:month>/<int:day>/', get_diet_data, name='get_diet_data'),
    path('post_diet_data/', post_diet_data, name='post_diet_data'),
    path('measurements/<int:year>/<int:month>/<int:day>/',  get_measurements, name='get_measurements'),
    path('post_measurements/<int:year>/<int:month>/<int:day>/', post_measurements, name='post_measurements'),
]
