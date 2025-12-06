import requests
from django.conf import settings


def send_email_via_lambda(action, to_email, data):
    """
    Call the serverless email Lambda/microservice.

    action: string like "SIGNUP_WELCOME" or "BOOKING_CONFIRMATION"
    to_email: recipient address
    data: dict with extra info (names, times, etc.)
    """
    if not settings.EMAIL_LAMBDA_URL:
        print("EMAIL: EMAIL_LAMBDA_URL not configured, skipping call")
        return

    payload = {
        "action": action,
        "to_email": to_email,
        "data": data,
    }

    try:
        resp = requests.post(settings.EMAIL_LAMBDA_URL, json=payload, timeout=5)
        print("EMAIL LAMBDA RESPONSE:", resp.status_code, resp.text)
    except Exception as e:
        print("EMAIL LAMBDA ERROR:", e)


def create_calendar_event_for_booking(booking):
    """
    Call the calendar Lambda/microservice to create Google Calendar events
    for both doctor and patient.
    """
    if not settings.CALENDAR_LAMBDA_URL:
        print("CALENDAR: CALENDAR_LAMBDA_URL not configured, skipping call")
        return

    doctor_profile = booking.doctor.profile
    patient_profile = booking.patient.profile

    payload = {
        "doctor_email": doctor_profile.google_email or booking.doctor.email,
        "patient_email": patient_profile.google_email or booking.patient.email,
        "start": booking.start_datetime.isoformat(),
        "end": booking.end_datetime.isoformat(),
        "doctor_name": booking.doctor.username,
        "patient_name": booking.patient.username,
        "google_client_id": settings.GOOGLE_CLIENT_ID,
        "google_client_secret": settings.GOOGLE_CLIENT_SECRET,
    }

    try:
        resp = requests.post(settings.CALENDAR_LAMBDA_URL, json=payload, timeout=5)
        print("CALENDAR LAMBDA RESPONSE:", resp.status_code, resp.text)
    except Exception as e:
        print("CALENDAR LAMBDA ERROR:", e)
