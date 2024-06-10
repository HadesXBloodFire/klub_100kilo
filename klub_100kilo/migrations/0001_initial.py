# Generated by Django 5.0.6 on 2024-06-10 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "Events",
            },
        ),
        migrations.CreateModel(
            name="Exercises",
            fields=[
                ("exercise_id", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.CharField(max_length=200)),
                ("muscle_group", models.CharField(max_length=60)),
                ("difficulty", models.CharField(max_length=50)),
                ("category", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "Exercises",
            },
        ),
        migrations.CreateModel(
            name="Gyms",
            fields=[
                ("gym_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=80)),
                ("phone_number", models.IntegerField()),
                ("address", models.CharField(max_length=80)),
            ],
            options={
                "db_table": "Gyms",
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("role", models.CharField(max_length=50)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("mail", models.CharField(max_length=100)),
                ("phone_number", models.IntegerField()),
                ("password", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "Users",
            },
        ),
        migrations.CreateModel(
            name="Trainers",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        db_column="user_ID",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="klub_100kilo.users",
                    ),
                ),
                ("hourly_cost", models.DecimalField(decimal_places=16, max_digits=16)),
                ("specialization", models.CharField(max_length=40)),
                ("description", models.CharField(max_length=400)),
            ],
            options={
                "db_table": "Trainers",
            },
        ),
        migrations.CreateModel(
            name="Reservations",
            fields=[
                ("reservation_id", models.AutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=50)),
                ("status", models.CharField(max_length=1)),
                ("trainer_id", models.IntegerField(blank=True, null=True)),
                ("date", models.DateTimeField()),
                (
                    "gym",
                    models.ForeignKey(
                        db_column="gym_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.gyms"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Reservations",
            },
        ),
        migrations.CreateModel(
            name="MeasurementsGoals",
            fields=[
                ("goal_id", models.AutoField(primary_key=True, serialize=False)),
                ("start_date", models.DateField()),
                ("max_days", models.IntegerField()),
                ("weight", models.IntegerField(blank=True, null=True)),
                ("biceps_size", models.IntegerField(blank=True, null=True)),
                ("bust_size", models.IntegerField(blank=True, null=True)),
                ("waist_size", models.IntegerField(blank=True, null=True)),
                ("thighs_size", models.IntegerField(blank=True, null=True)),
                ("height", models.IntegerField(blank=True, null=True)),
                ("status", models.CharField(default="N", max_length=1)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Measurements_Goals",
            },
        ),
        migrations.CreateModel(
            name="Measurements",
            fields=[
                ("date", models.DateField(primary_key=True, serialize=False)),
                ("weight", models.IntegerField(blank=True, null=True)),
                ("biceps_size", models.IntegerField(blank=True, null=True)),
                ("bust_size", models.IntegerField(blank=True, null=True)),
                ("waist_size", models.IntegerField(blank=True, null=True)),
                ("thighs_size", models.IntegerField(blank=True, null=True)),
                ("height", models.IntegerField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Measurements",
            },
        ),
        migrations.CreateModel(
            name="Diet",
            fields=[
                ("date", models.DateField(primary_key=True, serialize=False)),
                ("meal", models.CharField(max_length=100, null=True)),
                ("description", models.CharField(max_length=600, null=True)),
                ("calories", models.IntegerField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Diet",
            },
        ),
        migrations.CreateModel(
            name="TrainingGoals",
            fields=[
                ("goal_id", models.AutoField(primary_key=True, serialize=False)),
                ("start_date", models.DateField()),
                ("max_days", models.IntegerField()),
                ("muscle_group", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Training_Goals",
            },
        ),
        migrations.CreateModel(
            name="Trainings",
            fields=[
                ("training_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("took_place", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_ID", on_delete=django.db.models.deletion.DO_NOTHING, to="klub_100kilo.users"
                    ),
                ),
            ],
            options={
                "db_table": "Trainings",
            },
        ),
        migrations.CreateModel(
            name="TraningsExercises",
            fields=[
                ("training_exercise_id", models.AutoField(primary_key=True, serialize=False)),
                ("succeded", models.BooleanField(default=False)),
                (
                    "exercise",
                    models.ForeignKey(
                        db_column="exercise_ID",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="klub_100kilo.exercises",
                    ),
                ),
                (
                    "training",
                    models.ForeignKey(
                        db_column="training_ID",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="klub_100kilo.trainings",
                    ),
                ),
            ],
            options={
                "db_table": "Tranings_Exercises",
                "unique_together": {("training", "exercise")},
            },
        ),
        migrations.AddField(
            model_name="trainings",
            name="exercises",
            field=models.ManyToManyField(through="klub_100kilo.TraningsExercises", to="klub_100kilo.exercises"),
        ),
    ]
