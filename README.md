# 🚀 NextHire - Modern Flask Online Job Portal

NextHire is a modern, responsive, and full-featured Online Job Portal built with **Python 3**, **Flask**, **SQLAlchemy**, **Flask-Login**, **Flask-WTF**, and **Bootstrap 5**.

It provides a seamless experience for both **Job Seekers** looking for top opportunities and **Employers / Recruiters** managing end-to-end hiring pipelines.

---

## ✨ Key Features

### 👤 Dual User Roles & Authentication
- **Job Seeker (Candidate)**:
  - Register & customize candidate profile (headline, skills, experience, education, bio, and resume upload).
  - Search and filter jobs by keywords, categories, employment type, location, remote status, and salary sorting.
  - Apply for jobs using a profile resume or uploaded custom resume with tailored cover notes.
  - Interactive job bookmarking (AJAX-powered).
  - Candidate dashboard with live status tracker (*Pending*, *Reviewed*, *Shortlisted*, *Accepted*, *Rejected*).
  - Recommended job suggestions based on candidate skills.

- **Employer (Recruiter / Company)**:
  - Register and manage brand identity (company name, tagline, industry, website, location, logo upload, about story).
  - Post new job listings with rich parameters (experience levels, salary ranges, deadlines, required skills).
  - Manage existing job listings (edit, toggle active/closed status, delete).
  - Review candidate applications per job or across all postings.
  - View candidate qualifications, read cover notes, and download uploaded resumes.
  - Update candidate application status with instant dropdowns.

### 🎨 Modern & Stylish UI/UX
- Designed with modern tech typography (**Plus Jakarta Sans**).
- Glassmorphism navbar with backdrop blur and role-aware navigation.
- Responsive job search filter sidebar and card layouts with company logo badges.
- Dynamic toast notifications and micro-animations.

---

## 🛠️ Project Structure

```
jobportal/
├── app/
│   ├── __init__.py          # App factory, extensions, custom template filters
│   ├── models.py            # SQLAlchemy models (User, Profiles, Job, Category, Application, SavedJob)
│   ├── forms.py             # Flask-WTF forms for auth, profiles, job posts, applications
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Login, Register, Logout
│   │   ├── main.py          # Landing page, Job search, Details, Categories, Company profiles
│   │   ├── seeker.py        # Candidate dashboard, Applications, Bookmarks, Profile edit
│   │   └── employer.py      # Recruiter dashboard, Post job, Manage jobs, Review applicants
│   ├── static/
│   │   ├── css/style.css    # Custom modern styling
│   │   ├── js/main.js       # AJAX bookmarking, alerts, demo autofill
│   │   └── uploads/         # Uploaded resumes and company logos
│   └── templates/           # Jinja2 templates for all views
├── config.py                # App configuration (SQLite DB, Upload sizes, etc.)
├── run.py                   # App entrypoint
├── seed.py                  # Database seeder with realistic sample data
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
Make sure Python 3.10+ is installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Seed Database with Realistic Demo Data
Run the seeder to create sample categories, employers, job listings, candidates, and applications:
```bash
python seed.py
```

### 3. Start the Server
Launch the Flask development server:
```bash
python run.py
```
Open your browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Pre-seeded Demo Accounts

| Role | Email | Password | Features to Test |
| :--- | :--- | :--- | :--- |
| **Job Seeker** | `candidate@example.com` | `password123` | Search jobs, apply with resume, bookmark jobs, view application status timeline. |
| **Employer** | `recruiter@techcorp.com` | `password123` | Post jobs, manage listings, review candidate applicants, download resumes, update status. |
| **Employer 2** | `careers@innovatelabs.io` | `password123` | AI Labs company profile, review AI research engineer applicants. |

> **Tip:** You can also click the **"Quick Demo Fill"** buttons directly on the login page for 1-click credential filling!
