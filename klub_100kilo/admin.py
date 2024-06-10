from django.contrib import admin
from .models import Exercises, Gyms, Measurements, Reservations, Users, Diet


# Custom admin display for Exercises
@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = (
        "exercise_id",
        "description",
        "muscle_group",
        "difficulty",
        "category",
    )


# Custom admin display for Gyms
@admin.register(Gyms)
class GymsAdmin(admin.ModelAdmin):
    list_display = ("gym_id", "name", "phone_number", "address")


# Custom admin display for Measurements
@admin.register(Measurements)
class MeasurementsAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "user",
        "weight",
        "biceps_size",
        "bust_size",
        "waist_size",
        "thighs_size",
        "height",
    )


# Custom admin display for Reservations
@admin.register(Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'user', 'type', 'status', 'gym', 'trainer_id', 'name', 'start', 'end')
    list_filter = ("type", "status")


# Custom admin display for Users
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "role",
        "first_name",
        "last_name",
        "mail",
        "phone_number",
    )
    search_fields = ("first_name", "last_name", "mail")
    list_filter = ("role",)


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ("date", "user", "meal", "description", "calories")
