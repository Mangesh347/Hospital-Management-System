from django.contrib import admin
from .models import Profile, DoctorAvailability, Booking

admin.site.register(Profile)
admin.site.register(DoctorAvailability)
admin.site.register(Booking)
