from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    MinLengthValidator,
    RegexValidator,
)
from .models import MeasurementsGoals, Users


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, validators=[MinLengthValidator(1)]
    )
    last_name = forms.CharField(
        max_length=30, validators=[MinLengthValidator(1)]
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{9}$",
                message="Numer telefonu musi mieć dokładnie 9 cyfr.",
            )
        ],
    )
    email = forms.EmailField(max_length=254, validators=[EmailValidator()])
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                r"[A-Za-z0-9@#$%^&+=]",
                message="Hasło musi zawierać co najmniej jedną literę, jedną cyfrę i jeden znak specjalny.",
            ),
        ],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(validators=[EmailValidator()])
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        old_email = self.instance.email
        if new_email != old_email and User.objects.filter(email=new_email).exists():
            raise ValidationError("Email is already in use by another user.")
        return new_email

    def save(self, commit=True):
        user = super().save(commit=False)
        new_email = user.email
        old_email = User.objects.get(username=user.username).email

        users_model = Users.objects.get(mail=old_email)

        user.username = new_email
        if commit:
            user.save()
            users_model.first_name = user.first_name
            users_model.last_name = user.last_name
            users_model.mail = new_email
            users_model.save()
        return user

from django.contrib.auth import authenticate

class CustomPasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Obecne hasło",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Nowe hasło",
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                r"(?=.*\d)(?=.*[a-zA-Z])(?=.*[@#$%^&+=])",
                message="Hasło musi zawierać co najmniej jedną literę, jedną cyfrę i jeden znak specjalny.",
            ),
        ],
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")

        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Obecne hasło jest niepoprawne.")

        if old_password == new_password:
            raise forms.ValidationError("Nowe hasło musi być różne od obecnego.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
            users_model = Users.objects.get(mail=user.email)
            users_model.password = make_password(self.cleaned_data["new_password"])
            users_model.save()
        return user

class ReservationPanel(forms.Form):
    pass


class GoalForm(forms.ModelForm):
    class Meta:
        model = MeasurementsGoals
        fields = [
            "name",
            "start_date",
            "max_days",
            "weight",
            "biceps_size",
            "bust_size",
            "waist_size",
            "thighs_size",
            "height",
        ]
