from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    google_email = models.EmailField(blank=True, null=True)  # used later for calendar

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time}-{self.end_time}"


class Booking(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_bookings')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_bookings')
    slot = models.OneToOneField(DoctorAvailability, on_delete=models.PROTECT)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.patient.username} with {self.doctor.username} at {self.start_datetime}"
