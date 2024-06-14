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
from django.urls import path, re_path, include
from klub_100kilo.views import *
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="Klub 100kilo API",
        default_version="v1",
        description="API for Klub 100kilo",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reservations/", reservation_view, name="reservations"),
    path("", hero_page, name="hero_page"),
    path("main/", main_page, name="main_page"),
    path("signup/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", account, name="account"),
    path(
        "account/change_password/",
        auth_views.PasswordChangeView.as_view(
            template_name="change_password.html"
        ),
        name="change_password",
    ),
    path("account/edit_profile/", edit_profile, name="edit_profile"),
    path(
        "account/password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("book_trainer/", book_trainer, name="book_trainer"),
    path("measurements/", measurements_view, name="measurements"),
    path(
        "measurements/<int:year>/<int:month>/<int:day>/",
        get_measurements,
        name="get_measurements",
    ),
    path(
        "post_measurements/<int:year>/<int:month>/<int:day>/",
        post_measurements,
        name="post_measurements",
    ),
    path("diets/", diet_view, name="diet"),
    path(
        "diets/<int:year>/<int:month>/<int:day>/", get_diets, name="get_diets"
    ),
    path(
        "post_diets/<int:year>/<int:month>/<int:day>/",
        post_diets,
        name="post_diets",
    ),
    path("api/reservations/", get_reservations, name="get_reservations"),
    path("book_training/", book_training, name="book_training"),
    path("all_events/", all_events, name="all_events"),
    path("add_event/", add_event, name="add_event"),
    path("update/", update, name="update"),
    path("remove/", remove, name="remove"),
    path("goals/", goals_view, name="goals"),
    path("add_goal/", add_goal, name="add_goal"),
    path("delete_goal/<int:goal_id>/", delete_goal, name='delete_goal'),
    path("workouts/", workouts_view, name="workouts"),
    path("workouts/create_training/", create_training, name="create_training"),
    path("delete_training/<int:training_id>/", delete_training, name='delete_training'),
    path(
        "workouts/mark_exercises_as_succeeded/<int:training_id>/",
        mark_exercises_as_succeeded,
        name="mark_exercises_as_succeeded",
    ),
    path("", include("chat.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
