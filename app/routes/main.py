from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import or_
from app.models import db, Job, JobCategory, CompanyProfile, User, Application

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Featured / Latest active jobs
    latest_jobs = Job.query.filter_by(status='active').order_by(Job.created_at.desc()).limit(6).all()
    categories = JobCategory.query.all()
    top_companies = CompanyProfile.query.filter(CompanyProfile.company_name.isnot(None)).limit(4).all()
    
    # Platform metrics for hero section
    total_jobs = Job.query.filter_by(status='active').count()
    total_companies = CompanyProfile.query.count()
    total_seekers = User.query.filter_by(role='jobseeker').count()
    total_applications = Application.query.count()

    return render_template(
        'main/index.html',
        latest_jobs=latest_jobs,
        categories=categories,
        top_companies=top_companies,
        stats={
            'jobs': total_jobs or 120,
            'companies': total_companies or 45,
            'seekers': total_seekers or 850,
            'applications': total_applications or 1400
        }
    )


@main_bp.route('/jobs')
def jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 8

    # Filter parameters
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    job_type = request.args.get('job_type', '').strip()
    experience_level = request.args.get('experience_level', '').strip()
    location = request.args.get('location', '').strip()
    is_remote = request.args.get('is_remote') == '1'
    sort_by = request.args.get('sort_by', 'newest')

    # Base query for active jobs
    jobs_query = Job.query.filter_by(status='active')

    # Apply search keyword
    if query:
        search_pattern = f"%{query}%"
        jobs_query = jobs_query.join(Job.employer).join(User.company_profile).filter(
            or_(
                Job.title.ilike(search_pattern),
                Job.description.ilike(search_pattern),
                Job.skills_required.ilike(search_pattern),
                CompanyProfile.company_name.ilike(search_pattern),
                Job.location.ilike(search_pattern)
            )
        )

    # Apply filters
    if category_id:
        jobs_query = jobs_query.filter(Job.category_id == category_id)
    
    if job_type:
        jobs_query = jobs_query.filter(Job.job_type == job_type)

    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)

    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))

    if is_remote:
        jobs_query = jobs_query.filter(Job.is_remote.is_(True))

    # Apply sorting
    if sort_by == 'salary_high':
        jobs_query = jobs_query.order_by(Job.salary_max.desc().nullslast())
    elif sort_by == 'oldest':
        jobs_query = jobs_query.order_by(Job.created_at.asc())
    else:  # newest
        jobs_query = jobs_query.order_by(Job.created_at.desc())

    paginated_jobs = jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    categories = JobCategory.query.all()

    return render_template(
        'main/jobs.html',
        jobs=paginated_jobs.items,
        pagination=paginated_jobs,
        categories=categories,
        current_query=query,
        current_category=category_id,
        current_job_type=job_type,
        current_experience=experience_level,
        current_location=location,
        current_remote=is_remote,
        current_sort=sort_by
    )


@main_bp.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Increment views
    job.views_count = (job.views_count or 0) + 1
    db.session.commit()

    # Similar jobs in same category
    similar_jobs = Job.query.filter(
        Job.category_id == job.category_id,
        Job.id != job.id,
        Job.status == 'active'
    ).limit(3).all()

    # Form for apply modal
    from app.forms import ApplicationForm
    apply_form = ApplicationForm()

    has_applied = False
    is_saved = False
    from flask_login import current_user
    if current_user.is_authenticated and current_user.is_seeker:
        has_applied = current_user.has_applied_to(job.id)
        is_saved = current_user.has_saved(job.id)

    return render_template(
        'main/job_detail.html',
        job=job,
        similar_jobs=similar_jobs,
        apply_form=apply_form,
        has_applied=has_applied,
        is_saved=is_saved
    )


@main_bp.route('/categories')
def categories():
    all_categories = JobCategory.query.all()
    return render_template('main/categories.html', categories=all_categories)


@main_bp.route('/categories/<string:slug>')
def category_jobs(slug):
    category = JobCategory.query.filter_by(slug=slug).first_or_404()
    return redirect(url_for('main.jobs', category=category.id))


@main_bp.route('/companies/<int:company_id>')
def company_detail(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    active_jobs = Job.query.filter_by(employer_id=company.user_id, status='active').order_by(Job.created_at.desc()).all()
    return render_template('main/company_detail.html', company=company, active_jobs=active_jobs)
