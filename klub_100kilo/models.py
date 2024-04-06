# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Diet(models.Model):
    date = models.DateField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    breakfest = models.IntegerField()
    dinner = models.IntegerField()
    other = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diet'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Exercises(models.Model):
    exercise_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200)
    muscle_group = models.CharField(max_length=60)
    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'exercises'


class Gyms(models.Model):
    gym_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'gyms'


class Measurements(models.Model):
    date = models.DateField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    weight = models.IntegerField(blank=True, null=True)
    biceps_size = models.IntegerField(blank=True, null=True)
    bust_size = models.IntegerField(blank=True, null=True)
    waist_size = models.IntegerField(blank=True, null=True)
    dick_size = models.IntegerField(blank=True, null=True)
    thighs_size = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measurements'


class MeasurementsGoals(models.Model):
    goal_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    start_date = models.DateField()
    max_days = models.IntegerField()
    weight = models.IntegerField(blank=True, null=True)
    biceps_size = models.IntegerField(blank=True, null=True)
    bust_size = models.IntegerField(blank=True, null=True)
    waist_size = models.IntegerField(blank=True, null=True)
    dick_size = models.IntegerField(blank=True, null=True)
    thighs_size = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measurements_goals'


class Reservations(models.Model):
    reservation_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=1)
    gym = models.ForeignKey(Gyms, models.DO_NOTHING)
    trainer_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reservations'


class Trainers(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    hourly_cost = models.TextField()  # This field type is a guess.
    specialization = models.CharField(max_length=40)
    description = models.CharField(max_length=400)

    class Meta:
        managed = False
        db_table = 'trainers'


class TrainingGoals(models.Model):
    goal_id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    max_days = models.IntegerField()
    muscle_group = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'training_goals'


class Trainings(models.Model):
    training_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    trainer_id = models.IntegerField(blank=True, null=True)
    took_place = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'trainings'


class TraningExercises(models.Model):
    training = models.OneToOneField(Trainings, models.DO_NOTHING, primary_key=True)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING)
    succeded = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'traning_exercises'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'users'
