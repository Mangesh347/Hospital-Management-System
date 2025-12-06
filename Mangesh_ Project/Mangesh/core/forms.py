from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DoctorAvailability


class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    google_email = forms.EmailField(required=False, label="Google Calendar Email (optional)")

    class Meta:
        model = User
        fields = ('username', 'email', 'google_email', 'password1', 'password2')


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    google_email = forms.EmailField(required=False, label="Google Calendar Email (optional)")

    class Meta:
        model = User
        fields = ('username', 'email', 'google_email', 'password1', 'password2')


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ('date', 'start_time', 'end_time')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class BookingForm(forms.Form):
    slot_id = forms.IntegerField(widget=forms.HiddenInput())
