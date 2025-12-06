# Mini Hospital Management System (HMS)

## 1. Overview

This is a mini Hospital Management System built with **Django** and **PostgreSQL**.

- Doctors can **sign up** and publish their **availability slots**.
- Patients can **sign up**, browse doctors, and **book appointments**.
- An **Email Lambda microservice** is invoked on signup and booking.
- A **Calendar Lambda microservice** is invoked on booking to create Google Calendar events.

The project is designed as a **monolithic Django app** with integrations to two **serverless micro-services**.

---

## 2. Tech Stack

- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** Django templates (HTML), basic Bootstrap-ready layout
- **Environment config:** `.env` + `python-dotenv`
- **Integrations:**
  - Email microservice via HTTP (`EMAIL_LAMBDA_URL`)
  - Calendar microservice via HTTP (`CALENDAR_LAMBDA_URL`)

---

## 3. Project Structure (simplified)

```text
Shreya_Proj/
│ manage.py
│ .env
│ README.md
├─ hms/
│   ├─ settings.py
│   ├─ urls.py
│   └─ ...
├─ core/
│   ├─ models.py
│   ├─ views.py
│   ├─ forms.py
│   ├─ utils.py
│   ├─ decorators.py
│   ├─ urls.py
│   └─ admin.py
└─ templates/
    ├─ base.html
    ├─ home.html
    ├─ registration/
    │   ├─ login.html
    │   ├─ signup_doctor.html
    │   └─ signup_patient.html
    ├─ doctor/
    │   ├─ dashboard.html
    │   └─ availability_form.html
    └─ patient/
        ├─ dashboard.html
        └─ doctor_detail.html
