from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='jobseeker')  # 'jobseeker', 'employer', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    seeker_profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    posted_jobs = db.relationship('Job', backref='employer', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='seeker', lazy='dynamic', cascade='all, delete-orphan')
    saved_jobs = db.relationship('SavedJob', backref='seeker', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_seeker(self):
        return self.role == 'jobseeker'

    @property
    def is_employer(self):
        return self.role == 'employer'

    @property
    def display_name(self):
        if self.is_seeker and self.seeker_profile and self.seeker_profile.full_name:
            return self.seeker_profile.full_name
        if self.is_employer and self.company_profile and self.company_profile.company_name:
            return self.company_profile.company_name
        return self.username

    def has_applied_to(self, job_id):
        return self.applications.filter_by(job_id=job_id).first() is not None

    def has_saved(self, job_id):
        return self.saved_jobs.filter_by(job_id=job_id).first() is not None


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=True)
    headline = db.Column(db.String(150), nullable=True)  # e.g., "Senior Full-Stack Engineer"
    phone = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(300), nullable=True)  # Comma separated e.g., "Python, Flask, React, SQL"
    experience_years = db.Column(db.Integer, default=0)
    education = db.Column(db.String(200), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    avatar_filename = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)
    portfolio_url = db.Column(db.String(200), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def completion_percentage(self):
        fields = [self.full_name, self.headline, self.phone, self.location, self.bio, self.skills, self.resume_filename]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)


class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    tagline = db.Column(db.String(200), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)  # e.g., "10-50 employees", "500+ employees"
    website = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    logo_filename = db.Column(db.String(255), nullable=True)
    about = db.Column(db.Text, nullable=True)
    founded_year = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobCategory(db.Model):
    __tablename__ = 'job_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(80), nullable=False, unique=True, index=True)
    icon_class = db.Column(db.String(60), default='bi-briefcase')
    description = db.Column(db.String(255), nullable=True)
    
    jobs = db.relationship('Job', backref='category', lazy='dynamic')

    @property
    def active_jobs_count(self):
        return self.jobs.filter_by(status='active').count()


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('job_categories.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False, index=True)
    job_type = db.Column(db.String(40), default='Full-time')  # Full-time, Part-time, Remote, Contract, Internship
    experience_level = db.Column(db.String(40), default='Mid Level')  # Entry Level, Mid Level, Senior Level, Lead
    location = db.Column(db.String(100), nullable=False)
    is_remote = db.Column(db.Boolean, default=False)
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    salary_currency = db.Column(db.String(10), default='$')
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    skills_required = db.Column(db.String(255), nullable=True)  # Comma separated
    status = db.Column(db.String(20), default='active')  # 'active', 'closed', 'draft'
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    deadline = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy='dynamic', cascade='all, delete-orphan')
    saved_by = db.relationship('SavedJob', backref='job', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def skills_list(self):
        if not self.skills_required:
            return []
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    @property
    def formatted_salary(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency}{self.salary_min:,} - {self.salary_currency}{self.salary_max:,} / yr"
        elif self.salary_min:
            return f"From {self.salary_currency}{self.salary_min:,} / yr"
        elif self.salary_max:
            return f"Up to {self.salary_currency}{self.salary_max:,} / yr"
        return "Competitive / Negotiable"

    @property
    def applicants_count(self):
        return self.applications.count()


class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cover_note = db.Column(db.Text, nullable=True)
    resume_filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default='Pending')  # 'Pending', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted'
    employer_notes = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('job_id', 'seeker_id', name='unique_job_seeker_application'),
    )


class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('seeker_id', 'job_id', name='unique_saved_job'),
    )
