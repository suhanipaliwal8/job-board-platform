# Job Board Platform

A full-stack **Job Board Platform** built with **Django, Django REST Framework, PostgreSQL, HTML, CSS, and JavaScript**.

The platform provides separate workflows for **candidates and employers**, allowing employers to publish jobs and manage applications while candidates can search for jobs, upload resumes, apply for jobs, and manage their applications.

---

## Features

### Authentication & User Management

- User registration and login
- Session-based authentication
- Logout functionality
- Candidate and Employer roles
- Role-based access control
- User profile management

### Candidate Features

- Candidate dashboard
- Browse available jobs
- Search jobs by keywords
- Filter jobs by:
  - Location
  - Job type
  - Experience level
- View complete job details
- Upload/update resume
- Apply for jobs
- Add a cover letter
- View submitted applications
- Edit cover letters
- Withdraw applications
- Re-apply to withdrawn applications
- Track application status

### Employer Features

- Employer dashboard
- Create job listings
- Edit own job listings
- Delete/deactivate own job listings
- View applications received for own jobs
- View candidate information
- Access candidate resumes
- View cover letters
- Update application status
- Receive application notifications
- View application statistics

### Application Management

Supported application statuses:

```text
Applied
Shortlisted
Rejected
Selected
Withdrawn
```

The platform prevents duplicate applications for the same job.

Withdrawn applications are handled as a **soft delete**, allowing candidates to re-apply later.

### Security & Permissions

- Authentication required for protected operations
- Candidate-only endpoints
- Employer-only endpoints
- Employers can manage applications only for their own jobs
- Users cannot modify another user's resources
- CSRF protection for state-changing requests
- Session authentication
- Resume upload validation

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST APIs |
| PostgreSQL | Database |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| JavaScript | Frontend functionality |
| Git | Version control |
| GitHub | Repository hosting |

---

## Project Structure

```text
job-board-platform/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
│
├── applications/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── jobs/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── candidate_dashboard.html
│   ├── employer_dashboard.html
│   └── job_detail.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── media/
│   └── resumes/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd job-board-platform
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create a database named:

```text
job_board_db
```

Example PostgreSQL command:

```sql
CREATE DATABASE job_board_db;
```

Configure the database credentials in:

```text
config/settings.py
```

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "job_board_db",
        "USER": "postgres",
        "PASSWORD": "your_postgresql_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

> For production use, database credentials should be stored in environment variables rather than directly in `settings.py`.

---

## Database Migration

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

---

## Create Admin User

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Generate Test Data

The project includes a custom Django management command for generating test data.

Run:

```bash
python manage.py seed_data
```

This creates:

```text
5 Employers
10 Candidates
15 Jobs
```

All generated test accounts use:

```text
Password: Test@12345
```

### Example Employer

```text
Username: techflow_hr
Password: Test@12345
```

### Example Candidate

```text
Username: aarav_sharma
Password: Test@12345
```

The seed command uses `get_or_create`, so it can safely be executed again without creating duplicate test users/jobs.

---

## Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Application Workflow

## Candidate Workflow

```text
Register
   ↓
Login
   ↓
Candidate Dashboard
   ↓
Upload Resume
   ↓
Browse Jobs
   ↓
Search / Filter Jobs
   ↓
View Job Details
   ↓
Apply for Job
   ↓
Track Application
   ↓
Edit Cover Letter / Withdraw
   ↓
Re-apply if Withdrawn
```

## Employer Workflow

```text
Register
   ↓
Login
   ↓
Employer Dashboard
   ↓
Create Job
   ↓
Manage Job Listings
   ↓
Receive Applications
   ↓
View Candidate Details
   ↓
View Resume
   ↓
Review Cover Letter
   ↓
Update Application Status
   ↓
View Notifications & Statistics
```

---

## Application Status Flow

```text
Applied
   │
   ├──> Shortlisted
   │
   ├──> Rejected
   │
   └──> Selected
```

A candidate can also withdraw an application:

```text
Applied
   ↓
Withdrawn
   ↓
Re-apply
   ↓
Applied
```

Withdrawn applications cannot have their status changed by employers.

---

# REST API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/register/` | Register a user |
| POST | `/api/accounts/login/` | Login |
| POST | `/api/accounts/logout/` | Logout |
| GET | `/api/accounts/profile/` | Get current user profile |

## Jobs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs/` | List jobs |
| POST | `/api/jobs/` | Create a job |
| GET | `/api/jobs/<id>/` | Get job details |
| PUT/PATCH | `/api/jobs/<id>/` | Update own job |
| DELETE | `/api/jobs/<id>/` | Delete own job |

### Job Filters

The job listing API supports filters such as:

```text
/api/jobs/?search=python
/api/jobs/?location=Bengaluru
/api/jobs/?job_type=full_time
/api/jobs/?experience=fresher
```

Filters can also be combined.

## Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/applications/apply/` | Apply for a job |
| GET | `/api/applications/my/` | Candidate's applications |
| GET | `/api/applications/employer/` | Applications for employer's jobs |
| PATCH | `/api/applications/<id>/status/` | Update application status |
| PATCH | `/api/applications/<id>/update/` | Edit candidate cover letter |
| DELETE | `/api/applications/<id>/delete/` | Withdraw application |
| POST | `/api/applications/resume/` | Upload/update resume |
| GET | `/api/applications/resume/me/` | Get candidate resume |
| GET | `/api/applications/notifications/` | Employer notifications |

---

# User Roles

## Candidate

Candidates can:

- Browse jobs
- Search/filter jobs
- Upload resumes
- Apply for jobs
- Manage their own applications
- Withdraw applications
- Re-apply
- Edit cover letters

Candidates cannot:

- Create jobs
- Manage employer applications
- Change application statuses

## Employer

Employers can:

- Create jobs
- Manage their own jobs
- View applications for their jobs
- View candidate resumes
- Review cover letters
- Update application statuses
- View notifications
- View application statistics

Employers cannot manage jobs or applications belonging to other employers.

---

# Application Statistics

The employer dashboard provides application statistics including:

```text
Total Applications
Applied
Shortlisted
Rejected
Selected
```

These statistics are generated from applications received for the employer's jobs.

---

# Resume Management

Candidates can upload resumes in:

```text
PDF
DOC
DOCX
```

Uploaded resumes are associated with the candidate and can be accessed by employers when reviewing applications.

Resume files are stored through Django's media file handling.

---

# Notifications

When a candidate applies for a job, the corresponding employer receives a notification.

Notifications are also generated when a candidate re-applies after withdrawing an application.

Example:

```text
aarav_sharma applied for your job: Python Backend Developer
```

---

# Authentication

The application uses **Django session authentication**.

After successful login:

```text
User
 ↓
Django Session
 ↓
Authenticated API Requests
```

The frontend sends requests using browser session cookies.

CSRF protection is applied to state-changing requests.

---

# Testing

The application was tested for the following workflows.

### Candidate

- Registration
- Login/logout
- Resume upload
- Job browsing
- Job search
- Job filtering
- Job details
- Job application
- Duplicate application prevention
- Cover letter editing
- Application withdrawal
- Re-application

### Employer

- Registration
- Login/logout
- Job creation
- Job editing
- Job deletion
- Application management
- Resume viewing
- Cover letter viewing
- Application status updates
- Notifications
- Application statistics

### Authorization

- Candidate-only endpoints
- Employer-only endpoints
- Job ownership
- Application ownership
- Unauthorized access prevention

---

# Sample Credentials

For testing purposes, the seed command creates accounts using:

```text
Password: Test@12345
```

### Employer

```text
Username: techflow_hr
Password: Test@12345
```

### Candidate

```text
Username: aarav_sharma
Password: Test@12345
```

Additional test accounts are generated by:

```bash
python manage.py seed_data
```

> These are development/test credentials only and should not be used in a production environment.

---

# Environment Configuration

For production, sensitive values should be moved to environment variables.

Recommended variables:

```text
SECRET_KEY
DEBUG
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

Example:

```text
DB_NAME=job_board_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

# Future Improvements

Possible future enhancements include:

- Email notifications
- Advanced candidate profiles
- Company profiles
- Saved/bookmarked jobs
- Job recommendations
- Pagination
- Advanced resume parsing
- Application analytics
- Employer search
- Password reset through email
- Social authentication
- Automated testing with pytest
- Docker deployment
- Cloud deployment
- Production environment configuration

---

# Development Commands

### Start Server

```bash
python manage.py runserver
```

### Create Migrations

```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Admin

```bash
python manage.py createsuperuser
```

### Generate Test Data

```bash
python manage.py seed_data
```

### Collect Static Files

```bash
python manage.py collectstatic
```

---

# Git Workflow

The project is maintained using Git.

```bash
git init
git add .
git commit -m "Complete job board platform features"
git push
```

---

# Project Status

**Status: Completed**

The platform currently provides a complete job-board workflow for candidates and employers, including authentication, job management, applications, resume handling, notifications, statistics, and role-based permissions.

---

## Author

**Suhani Paliwal**

B.Tech — Computer Science & Data Science

Built as part of a backend development internship project.
