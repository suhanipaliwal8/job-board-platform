from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import Profile
from jobs.models import Job


class Command(BaseCommand):
    help = "Create fake employers, candidates and jobs for testing"

    def handle(self, *args, **kwargs):

        # ==========================================================
        # EMPLOYERS
        # ==========================================================

        employers_data = [
            {
                "username": "techflow_hr",
                "email": "hr@techflow.example.com",
                "company_name": "TechFlow Solutions",
                "phone": "9876501001",
            },
            {
                "username": "novabyte_hr",
                "email": "careers@novabyte.example.com",
                "company_name": "NovaByte Technologies",
                "phone": "9876501002",
            },
            {
                "username": "cloudnest_hr",
                "email": "hr@cloudnest.example.com",
                "company_name": "CloudNest Systems",
                "phone": "9876501003",
            },
            {
                "username": "datapulse_hr",
                "email": "careers@datapulse.example.com",
                "company_name": "DataPulse Analytics",
                "phone": "9876501004",
            },
            {
                "username": "innovex_hr",
                "email": "jobs@innovex.example.com",
                "company_name": "Innovex Labs",
                "phone": "9876501005",
            },
        ]

        employers = {}

        for data in employers_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                },
            )

            if created:
                user.set_password("Test@12345")
                user.save()

            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": "employer",
                    "phone": data["phone"],
                    "company_name": data["company_name"],
                },
            )

            employers[data["username"]] = user

            self.stdout.write(
                self.style.SUCCESS(
                    f"Employer created/updated: {data['username']}"
                )
            )

        # ==========================================================
        # CANDIDATES
        # ==========================================================

        candidates_data = [
            ("aarav_sharma", "aarav@example.com", "9876510001"),
            ("ananya_verma", "ananya@example.com", "9876510002"),
            ("rohan_mehta", "rohan@example.com", "9876510003"),
            ("isha_gupta", "isha@example.com", "9876510004"),
            ("vivaan_patel", "vivaan@example.com", "9876510005"),
            ("meera_kapoor", "meera@example.com", "9876510006"),
            ("aditya_singh", "aditya@example.com", "9876510007"),
            ("kavya_jain", "kavya@example.com", "9876510008"),
            ("arjun_malhotra", "arjun@example.com", "9876510009"),
            ("simran_kaur", "simran@example.com", "9876510010"),
        ]

        for username, email, phone in candidates_data:

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                },
            )

            if created:
                user.set_password("Test@12345")
                user.save()

            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": "candidate",
                    "phone": phone,
                    "company_name": "",
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Candidate created/updated: {username}"
                )
            )

        # ==========================================================
        # JOBS
        # ==========================================================

        jobs_data = [
            {
                "title": "Python Backend Developer",
                "description": (
                    "We are looking for a Python Backend Developer to design, "
                    "develop, and maintain reliable backend services and REST APIs. "
                    "The candidate will work with the engineering team to build "
                    "scalable applications, integrate databases, write clean and "
                    "maintainable code, and troubleshoot production issues. "
                    "Experience with Django or FastAPI is preferred."
                ),
                "company_name": "TechFlow Solutions",
                "location": "Bengaluru, Karnataka",
                "salary": "6-10 LPA",
                "skills": "Python, Django, FastAPI, REST API, PostgreSQL, Git",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "techflow_hr",
            },
            {
                "title": "Frontend Developer",
                "description": (
                    "Join our frontend engineering team to build responsive "
                    "and user-friendly web applications. You will work closely "
                    "with designers and backend developers to implement reusable "
                    "UI components, improve application performance, and ensure "
                    "a consistent user experience across devices."
                ),
                "company_name": "TechFlow Solutions",
                "location": "Pune, Maharashtra",
                "salary": "5-8 LPA",
                "skills": "HTML, CSS, JavaScript, React, Git, REST API",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "techflow_hr",
            },
            {
                "title": "Software Engineering Intern",
                "description": (
                    "This internship is designed for students who want practical "
                    "software development experience. Interns will contribute to "
                    "real development tasks, write and test code, work with Git, "
                    "participate in code reviews, and learn software development "
                    "practices from experienced engineers."
                ),
                "company_name": "TechFlow Solutions",
                "location": "Remote",
                "salary": "15000-25000 per month",
                "skills": "Python, JavaScript, Git, SQL, Problem Solving",
                "job_type": "internship",
                "experience": "fresher",
                "employer": "techflow_hr",
            },
            {
                "title": "Django Developer",
                "description": (
                    "NovaByte Technologies is hiring a Django Developer to "
                    "develop secure and scalable web applications. The role "
                    "includes designing backend modules, creating REST APIs, "
                    "integrating PostgreSQL databases, implementing authentication, "
                    "writing automated tests, and collaborating with frontend developers."
                ),
                "company_name": "NovaByte Technologies",
                "location": "Hyderabad, Telangana",
                "salary": "7-11 LPA",
                "skills": "Python, Django, Django REST Framework, PostgreSQL, REST API",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "novabyte_hr",
            },
            {
                "title": "Java Developer",
                "description": (
                    "We are seeking a Java Developer to build and maintain "
                    "enterprise software applications. The role involves "
                    "implementing business logic, developing APIs, writing unit "
                    "tests, debugging issues, and working with relational databases."
                ),
                "company_name": "NovaByte Technologies",
                "location": "Chennai, Tamil Nadu",
                "salary": "6-12 LPA",
                "skills": "Java, Spring Boot, REST API, SQL, Git, OOP",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "novabyte_hr",
            },
            {
                "title": "QA Automation Intern",
                "description": (
                    "We are looking for a QA Automation Intern to assist in "
                    "creating and maintaining automated test cases. The intern "
                    "will learn software testing methodologies, identify bugs, "
                    "document test results, and work with developers to improve "
                    "application quality."
                ),
                "company_name": "NovaByte Technologies",
                "location": "Noida, Uttar Pradesh",
                "salary": "12000-18000 per month",
                "skills": "Python, Selenium, Testing, SQL, Git",
                "job_type": "internship",
                "experience": "fresher",
                "employer": "novabyte_hr",
            },
            {
                "title": "Cloud Engineer",
                "description": (
                    "CloudNest Systems is hiring a Cloud Engineer to help design, "
                    "deploy, and maintain cloud infrastructure. The candidate will "
                    "work on cloud resources, deployment automation, monitoring, "
                    "security configurations, and troubleshooting."
                ),
                "company_name": "CloudNest Systems",
                "location": "Mumbai, Maharashtra",
                "salary": "8-14 LPA",
                "skills": "AWS, Linux, Docker, Kubernetes, Networking, CI/CD",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "cloudnest_hr",
            },
            {
                "title": "DevOps Engineer",
                "description": (
                    "We are looking for a DevOps Engineer to improve application "
                    "deployment and infrastructure reliability. The role includes "
                    "maintaining CI/CD pipelines, managing containerized applications, "
                    "monitoring systems, automating repetitive tasks, and collaborating "
                    "with development teams."
                ),
                "company_name": "CloudNest Systems",
                "location": "Bengaluru, Karnataka",
                "salary": "10-16 LPA",
                "skills": "Docker, Kubernetes, AWS, Jenkins, Linux, CI/CD, Terraform",
                "job_type": "full_time",
                "experience": "3-5",
                "employer": "cloudnest_hr",
            },
            {
                "title": "Cloud Support Associate",
                "description": (
                    "The Cloud Support Associate will assist customers and internal "
                    "teams with cloud infrastructure issues. Responsibilities include "
                    "monitoring services, troubleshooting connectivity and deployment "
                    "problems, documenting incidents, and escalating complex issues."
                ),
                "company_name": "CloudNest Systems",
                "location": "Gurugram, Haryana",
                "salary": "4-7 LPA",
                "skills": "AWS, Linux, Networking, Troubleshooting, Python",
                "job_type": "full_time",
                "experience": "fresher",
                "employer": "cloudnest_hr",
            },
            {
                "title": "Data Analyst",
                "description": (
                    "DataPulse Analytics is looking for a Data Analyst to transform "
                    "raw business data into meaningful insights. The candidate will "
                    "clean datasets, perform exploratory analysis, build reports and "
                    "dashboards, identify trends, and communicate findings to stakeholders."
                ),
                "company_name": "DataPulse Analytics",
                "location": "Pune, Maharashtra",
                "salary": "5-9 LPA",
                "skills": "Python, SQL, Excel, Pandas, Data Visualization, Power BI",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "datapulse_hr",
            },
            {
                "title": "Machine Learning Intern",
                "description": (
                    "This internship provides an opportunity to work on practical "
                    "machine learning problems. The intern will assist with data "
                    "preprocessing, exploratory analysis, feature engineering, "
                    "model training, evaluation, and documentation."
                ),
                "company_name": "DataPulse Analytics",
                "location": "Remote",
                "salary": "15000-22000 per month",
                "skills": "Python, Pandas, NumPy, Scikit-learn, Machine Learning, SQL",
                "job_type": "internship",
                "experience": "fresher",
                "employer": "datapulse_hr",
            },
            {
                "title": "Senior Data Engineer",
                "description": (
                    "DataPulse Analytics is seeking an experienced Data Engineer "
                    "to design and maintain reliable data pipelines and platforms. "
                    "The role involves building ETL workflows, optimizing data "
                    "processing systems, working with databases and cloud services, "
                    "and collaborating with analytics and machine learning teams."
                ),
                "company_name": "DataPulse Analytics",
                "location": "Bengaluru, Karnataka",
                "salary": "18-28 LPA",
                "skills": "Python, SQL, Spark, Airflow, AWS, Data Engineering, ETL",
                "job_type": "full_time",
                "experience": "5+",
                "employer": "datapulse_hr",
            },
            {
                "title": "Full Stack Developer",
                "description": (
                    "Innovex Labs is hiring a Full Stack Developer to develop "
                    "complete web applications from frontend interfaces to backend "
                    "APIs. The candidate will work with product and design teams, "
                    "implement new features, integrate databases, optimize application "
                    "performance, and participate in testing and deployment."
                ),
                "company_name": "Innovex Labs",
                "location": "Indore, Madhya Pradesh",
                "salary": "6-10 LPA",
                "skills": "Python, Django, React, JavaScript, PostgreSQL, REST API",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "innovex_hr",
            },
            {
                "title": "Backend Developer",
                "description": (
                    "Innovex Labs is looking for a Backend Developer to build APIs "
                    "and server-side services for our applications. The candidate "
                    "will design database models, implement business logic, integrate "
                    "third-party services, write tests, and improve backend performance."
                ),
                "company_name": "Innovex Labs",
                "location": "Bhopal, Madhya Pradesh",
                "salary": "5-9 LPA",
                "skills": "Python, FastAPI, Django, PostgreSQL, REST API, Docker",
                "job_type": "full_time",
                "experience": "1-2",
                "employer": "innovex_hr",
            },
            {
                "title": "Product Engineering Intern",
                "description": (
                    "Innovex Labs is offering a Product Engineering Internship "
                    "for students interested in building software products. Interns "
                    "will work with developers on feature implementation, debugging, "
                    "testing, API integration, and documentation. This role provides "
                    "exposure to the complete software development lifecycle."
                ),
                "company_name": "Innovex Labs",
                "location": "Indore, Madhya Pradesh",
                "salary": "10000-18000 per month",
                "skills": "Python, JavaScript, SQL, Git, REST API, Problem Solving",
                "job_type": "internship",
                "experience": "fresher",
                "employer": "innovex_hr",
            },
        ]

        # ==========================================================
        # CREATE JOBS
        # ==========================================================

        for job_data in jobs_data:

            employer = employers[job_data["employer"]]

            Job.objects.get_or_create(
                title=job_data["title"],
                employer=employer,
                defaults={
                    "description": job_data["description"],
                    "company_name": job_data["company_name"],
                    "location": job_data["location"],
                    "salary": job_data["salary"],
                    "skills": job_data["skills"],
                    "job_type": job_data["job_type"],
                    "experience": job_data["experience"],
                    "is_active": True,
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Job created: {job_data['title']}"
                )
            )

        # ==========================================================
        # SUMMARY
        # ==========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("======================================")
        )
        self.stdout.write(
            self.style.SUCCESS("      SEED DATA CREATED SUCCESSFULLY")
        )
        self.stdout.write(
            self.style.SUCCESS("======================================")
        )
        self.stdout.write(
            self.style.SUCCESS("Employers : 5")
        )
        self.stdout.write(
            self.style.SUCCESS("Candidates: 10")
        )
        self.stdout.write(
            self.style.SUCCESS("Jobs      : 15")
        )
        self.stdout.write(
            self.style.SUCCESS("Password  : Test@12345")
        )
        self.stdout.write(
            self.style.SUCCESS("======================================")
        )