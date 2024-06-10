from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "Users"


class Exercises(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    muscle_group = models.CharField(max_length=60)
    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    class Meta:
        db_table = "Exercises"


class Gyms(models.Model):
    gym_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=80)

    class Meta:
        db_table = "Gyms"


class Measurements(models.Model):
    date = models.DateField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, db_column="user_ID"
    )
    weight = models.IntegerField(blank=True, null=True)
    biceps_size = models.IntegerField(blank=True, null=True)
    bust_size = models.IntegerField(blank=True, null=True)
    waist_size = models.IntegerField(blank=True, null=True)
    thighs_size = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "Measurements"


class MeasurementsGoals(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, db_column="user_ID"
    )
    start_date = models.DateField()
    max_days = models.IntegerField()
    weight = models.IntegerField(blank=True, null=True)
    biceps_size = models.IntegerField(blank=True, null=True)
    bust_size = models.IntegerField(blank=True, null=True)
    waist_size = models.IntegerField(blank=True, null=True)
    thighs_size = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, default='N')  # Add this line

    class Meta:
        db_table = "Measurements_Goals"


class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, db_column="user_ID"
    )
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=1)
    gym = models.ForeignKey(
        Gyms, on_delete=models.CASCADE, db_column="gym_ID"
    )
    trainer_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.start < timezone.now() or self.end < timezone.now():
            raise ValidationError("Start and end times cannot be in the past")

        overlapping_reservations = Reservations.objects.filter(
            user=self.user,
            start__lt=self.end,
            end__gt=self.start
        )

        if self.pk:
            overlapping_reservations = overlapping_reservations.exclude(pk=self.pk)

        if overlapping_reservations.exists():
            raise ValidationError("You have another reservation at the same time")


    class Meta:
        db_table = "Reservations"


class Trainers(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.DO_NOTHING,
        db_column="user_ID",
        primary_key=True,
    )
    hourly_cost = models.DecimalField(max_digits=16, decimal_places=16)
    specialization = models.CharField(max_length=40)
    description = models.CharField(max_length=400)

    class Meta:
        db_table = "Trainers"


class TrainingGoals(models.Model):
    goal_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    max_days = models.IntegerField()
    muscle_group = models.IntegerField()
    user = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, db_column="user_ID"
    )

    class Meta:
        db_table = "Training_Goals"


class Trainings(models.Model):
    training_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, db_column="user_ID"
    )
    took_place = models.BooleanField(default=False)
    exercises = models.ManyToManyField(Exercises, through='TraningsExercises')

    class Meta:
        db_table = "Trainings"


class TraningsExercises(models.Model):
    training_exercise_id = models.AutoField(primary_key=True)
    training = models.ForeignKey(
        Trainings,
        on_delete=models.DO_NOTHING,
        db_column="training_ID",
    )
    exercise = models.ForeignKey(
        Exercises, on_delete=models.DO_NOTHING, db_column="exercise_ID"
    )
    succeded = models.BooleanField(default=False)

    class Meta:
        db_table = "Tranings_Exercises"
        unique_together = (("training", "exercise"),)

class Diet(models.Model):
    date = models.DateField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column="user_ID")
    meal = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=600, null=True)
    calories = models.IntegerField(null=True)

    class Meta:
        db_table = "Diet"



class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Events"
