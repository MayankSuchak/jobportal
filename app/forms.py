from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField,
    SelectField, IntegerField, URLField, DateField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError
)
from app.models import User, JobCategory

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')


class JobSeekerRegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Candidate Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken. Please choose another.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email address is already registered.')


class EmployerRegisterForm(FlaskForm):
    company_name = StringField('Company / Organization Name', validators=[DataRequired(), Length(max=150)])
    industry = StringField('Industry / Sector', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Business Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Employer Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken. Please choose another.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email address is already registered.')


class JobSeekerProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    headline = StringField('Professional Headline', validators=[Optional(), Length(max=150)], 
                           render_kw={"placeholder": "e.g., Senior Full-Stack Python & React Developer"})
    phone = StringField('Phone Number', validators=[Optional(), Length(max=30)])
    location = StringField('Location / City', validators=[Optional(), Length(max=100)],
                           render_kw={"placeholder": "e.g., San Francisco, CA or Remote"})
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
    education = StringField('Highest Education', validators=[Optional(), Length(max=200)],
                            render_kw={"placeholder": "e.g., B.S. in Computer Science - Stanford"})
    skills = StringField('Key Skills (comma-separated)', validators=[Optional(), Length(max=300)],
                         render_kw={"placeholder": "e.g., Python, Flask, React, PostgreSQL, Docker"})
    bio = TextAreaField('About Me / Summary', validators=[Optional(), Length(max=2000)],
                        render_kw={"rows": 4, "placeholder": "Share a brief overview of your background and career goals..."})
    resume = FileField('Upload Resume (PDF, DOCX - max 10MB)', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents allowed!')])
    linkedin_url = URLField('LinkedIn Profile', validators=[Optional(), Length(max=200)])
    github_url = URLField('GitHub Profile', validators=[Optional(), Length(max=200)])
    portfolio_url = URLField('Portfolio / Personal Website', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Profile')


class CompanyProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=150)])
    tagline = StringField('Tagline / Slogan', validators=[Optional(), Length(max=200)],
                          render_kw={"placeholder": "e.g., Building the next generation of cloud infrastructure"})
    industry = StringField('Industry / Sector', validators=[DataRequired(), Length(max=100)],
                           render_kw={"placeholder": "e.g., Financial Technology, AI & Data, Healthcare"})
    company_size = SelectField('Company Size', choices=[
        ('', 'Select Company Size'),
        ('1-10 employees', '1-10 employees (Startup)'),
        ('11-50 employees', '11-50 employees (Small)'),
        ('51-200 employees', '51-200 employees (Medium)'),
        ('201-500 employees', '201-500 employees (Mid-Market)'),
        ('500+ employees', '500+ employees (Enterprise)')
    ], validators=[Optional()])
    website = URLField('Company Website', validators=[Optional(), Length(max=200)],
                       render_kw={"placeholder": "https://example.com"})
    location = StringField('Headquarters / Location', validators=[Optional(), Length(max=100)],
                           render_kw={"placeholder": "e.g., New York, NY"})
    founded_year = IntegerField('Founded Year', validators=[Optional(), NumberRange(min=1800, max=2030)])
    about = TextAreaField('About Company / Culture', validators=[Optional(), Length(max=3000)],
                          render_kw={"rows": 5, "placeholder": "Describe your company mission, culture, and what it's like to work here..."})
    logo = FileField('Company Logo', validators=[Optional(), FileAllowed(['png', 'jpg', 'jpeg', 'webp', 'svg'], 'Images only!')])
    submit = SubmitField('Update Company Profile')


class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=150)],
                        render_kw={"placeholder": "e.g., Senior Backend Engineer (Python/Flask)"})
    category_id = SelectField('Job Category', coerce=int, validators=[DataRequired()])
    job_type = SelectField('Employment Type', choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote (Full-time)'),
        ('Contract', 'Contract / Freelance'),
        ('Internship', 'Internship')
    ], validators=[DataRequired()])
    experience_level = SelectField('Experience Level', choices=[
        ('Entry Level', 'Entry Level (0-2 years)'),
        ('Mid Level', 'Mid Level (2-5 years)'),
        ('Senior Level', 'Senior Level (5+ years)'),
        ('Lead / Executive', 'Lead / Principal / Executive')
    ], validators=[DataRequired()])
    location = StringField('Job Location', validators=[DataRequired(), Length(max=100)],
                           render_kw={"placeholder": "e.g., San Francisco, CA (or Remote)"})
    is_remote = BooleanField('Open for 100% Remote Candidates')
    salary_currency = SelectField('Currency', choices=[('$', 'USD ($)'), ('€', 'EUR (€)'), ('£', 'GBP (£)'), ('₹', 'INR (₹)')], default='$')
    salary_min = IntegerField('Minimum Salary (Annual)', validators=[Optional(), NumberRange(min=0)])
    salary_max = IntegerField('Maximum Salary (Annual)', validators=[Optional(), NumberRange(min=0)])
    skills_required = StringField('Required Skills (comma-separated)', validators=[Optional(), Length(max=255)],
                                  render_kw={"placeholder": "e.g., Python, Docker, PostgreSQL, AWS"})
    description = TextAreaField('Job Description', validators=[DataRequired()],
                                render_kw={"rows": 6, "placeholder": "Provide a detailed overview of the role, responsibilities, and team mission..."})
    requirements = TextAreaField('Requirements & Qualifications', validators=[Optional()],
                                 render_kw={"rows": 5, "placeholder": "• 3+ years experience with Python\n• Strong knowledge of relational databases\n• Experience with RESTful APIs"})
    benefits = TextAreaField('Benefits & Perks', validators=[Optional()],
                             render_kw={"rows": 4, "placeholder": "• Competitive compensation & equity\n• Health, dental & vision insurance\n• 401(k) matching\n• Flexible remote work"})
    status = SelectField('Status', choices=[('active', 'Active (Published)'), ('closed', 'Closed'), ('draft', 'Draft')], default='active')
    deadline = DateField('Application Deadline', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Publish Job Listing')


class ApplicationForm(FlaskForm):
    cover_note = TextAreaField('Cover Letter / Note to Recruiter', validators=[Optional(), Length(max=2500)],
                               render_kw={"rows": 4, "placeholder": "Explain why you're a great fit for this role and highlight your most relevant achievements..."})
    resume = FileField('Upload Custom Resume (Optional if already in profile)', 
                       validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'PDF and DOCX files only')])
    use_profile_resume = BooleanField('Use resume from my profile', default=True)
    submit = SubmitField('Submit Application')
