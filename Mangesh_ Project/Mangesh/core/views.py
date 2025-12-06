from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.utils import timezone
from django.contrib.auth.models import User

from .forms import (
    DoctorSignUpForm,
    PatientSignUpForm,
    AvailabilityForm,
    BookingForm,
)
from .models import Profile, DoctorAvailability, Booking
from .decorators import doctor_required, patient_required
from .utils import send_email_via_lambda, create_calendar_event_for_booking


def home(request):
    return render(request, 'home.html')


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            google_email = form.cleaned_data.get('google_email')
            Profile.objects.create(user=user, role='DOCTOR', google_email=google_email)
            # Welcome email (stub)
            send_email_via_lambda(
                'SIGNUP_WELCOME',
                user.email,
                {'name': user.username, 'role': 'Doctor'}
            )
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'registration/signup_doctor.html', {'form': form})


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            google_email = form.cleaned_data.get('google_email')
            Profile.objects.create(user=user, role='PATIENT', google_email=google_email)
            # Welcome email (stub)
            send_email_via_lambda(
                'SIGNUP_WELCOME',
                user.email,
                {'name': user.username, 'role': 'Patient'}
            )
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'registration/signup_patient.html', {'form': form})


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    else:
        return redirect('patient_dashboard')


@doctor_required
def doctor_dashboard(request):
    slots = DoctorAvailability.objects.filter(doctor=request.user)
    bookings = Booking.objects.filter(doctor=request.user).select_related('patient', 'slot')
    return render(request, 'doctor/dashboard.html', {
        'slots': slots,
        'bookings': bookings,
    })


@doctor_required
def add_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            return redirect('doctor_dashboard')
    else:
        form = AvailabilityForm()
    return render(request, 'doctor/availability_form.html', {'form': form})


@patient_required
def patient_dashboard(request):
    doctors = User.objects.filter(profile__role='DOCTOR')
    return render(request, 'patient/dashboard.html', {'doctors': doctors})


@patient_required
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, profile__role='DOCTOR')
    today = timezone.now().date()
    now_time = timezone.now().time()

    # Future, not booked slots
    slots = DoctorAvailability.objects.filter(
        doctor=doctor,
        is_booked=False
    ).filter(
        models.Q(date__gt=today) |
        (models.Q(date=today) & models.Q(start_time__gt=now_time))
    )

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            slot_id = form.cleaned_data['slot_id']
            with transaction.atomic():
                slot = DoctorAvailability.objects.select_for_update().get(
                    id=slot_id,
                    doctor=doctor,
                )
                if slot.is_booked:
                    # someone booked it already
                    return redirect('doctor_detail', doctor_id=doctor.id)

                slot.is_booked = True
                slot.save()

                start_dt = timezone.make_aware(
                    datetime.combine(slot.date, slot.start_time)
                )
                end_dt = timezone.make_aware(
                    datetime.combine(slot.date, slot.end_time)
                )

                booking = Booking.objects.create(
                    doctor=doctor,
                    patient=request.user,
                    slot=slot,
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                )

                # Booking email (stub)
                send_email_via_lambda(
                    'BOOKING_CONFIRMATION',
                    request.user.email,
                    {
                        'patient': request.user.username,
                        'doctor': doctor.username,
                        'start': str(start_dt),
                        'end': str(end_dt),
                    }
                )

                # Calendar event (stub)
                create_calendar_event_for_booking(booking)

                return redirect('patient_dashboard')
    else:
        form = BookingForm()

    return render(request, 'patient/doctor_detail.html', {
        'doctor': doctor,
        'slots': slots,
        'form': form,
    })
