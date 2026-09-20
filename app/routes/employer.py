import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db, employer_required
from app.models import CompanyProfile, JobCategory, Job, Application
from app.forms import CompanyProfileForm, JobPostForm

employer_bp = Blueprint('employer', __name__)

def save_uploaded_file(file, folder, allowed_extensions):
    if not file or not file.filename:
        return None
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in allowed_extensions:
        return None
    unique_filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
    file_path = os.path.join(folder, unique_filename)
    file.save(file_path)
    return unique_filename


@employer_bp.route('/dashboard')
@employer_required
def dashboard():
    company = current_user.company_profile
    posted_jobs = current_user.posted_jobs.order_by(Job.created_at.desc()).all()
    
    # Calculate stats
    total_jobs = len(posted_jobs)
    active_jobs = sum(1 for j in posted_jobs if j.status == 'active')
    
    all_job_ids = [j.id for j in posted_jobs]
    recent_applications = Application.query.filter(
        Application.job_id.in_(all_job_ids)
    ).order_by(Application.applied_at.desc()).limit(8).all() if all_job_ids else []

    total_applicants = Application.query.filter(
        Application.job_id.in_(all_job_ids)
    ).count() if all_job_ids else 0

    pending_reviews = Application.query.filter(
        Application.job_id.in_(all_job_ids),
        Application.status == 'Pending'
    ).count() if all_job_ids else 0

    shortlisted_count = Application.query.filter(
        Application.job_id.in_(all_job_ids),
        Application.status == 'Shortlisted'
    ).count() if all_job_ids else 0

    return render_template(
        'employer/dashboard.html',
        company=company,
        posted_jobs=posted_jobs[:5],
        total_jobs=total_jobs,
        active_jobs=active_jobs,
        total_applicants=total_applicants,
        pending_reviews=pending_reviews,
        shortlisted_count=shortlisted_count,
        recent_applications=recent_applications
    )


@employer_bp.route('/post-job', methods=['GET', 'POST'])
@employer_required
def post_job():
    form = JobPostForm()
    form.category_id.choices = [(c.id, c.name) for c in JobCategory.query.order_by(JobCategory.name).all()]

    if form.validate_on_submit():
        job = Job(
            employer_id=current_user.id,
            category_id=form.category_id.data,
            title=form.title.data.strip(),
            job_type=form.job_type.data,
            experience_level=form.experience_level.data,
            location=form.location.data.strip(),
            is_remote=form.is_remote.data,
            salary_currency=form.salary_currency.data,
            salary_min=form.salary_min.data,
            salary_max=form.salary_max.data,
            skills_required=form.skills_required.data,
            description=form.description.data,
            requirements=form.requirements.data,
            benefits=form.benefits.data,
            status=form.status.data,
            deadline=form.deadline.data
        )
        db.session.add(job)
        db.session.commit()

        flash(f'Job listing "{job.title}" has been published successfully!', 'success')
        return redirect(url_for('employer.manage_jobs'))

    return render_template('employer/post_job.html', form=form)


@employer_bp.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@employer_required
def edit_job(job_id):
    job = Job.query.filter_by(id=job_id, employer_id=current_user.id).first_or_404()
    form = JobPostForm(obj=job)
    form.category_id.choices = [(c.id, c.name) for c in JobCategory.query.order_by(JobCategory.name).all()]

    if form.validate_on_submit():
        job.title = form.title.data.strip()
        job.category_id = form.category_id.data
        job.job_type = form.job_type.data
        job.experience_level = form.experience_level.data
        job.location = form.location.data.strip()
        job.is_remote = form.is_remote.data
        job.salary_currency = form.salary_currency.data
        job.salary_min = form.salary_min.data
        job.salary_max = form.salary_max.data
        job.skills_required = form.skills_required.data
        job.description = form.description.data
        job.requirements = form.requirements.data
        job.benefits = form.benefits.data
        job.status = form.status.data
        job.deadline = form.deadline.data

        db.session.commit()
        flash(f'Job listing "{job.title}" updated successfully!', 'success')
        return redirect(url_for('employer.manage_jobs'))

    return render_template('employer/edit_job.html', form=form, job=job)


@employer_bp.route('/manage-jobs')
@employer_required
def manage_jobs():
    jobs = current_user.posted_jobs.order_by(Job.created_at.desc()).all()
    return render_template('employer/manage_jobs.html', jobs=jobs)


@employer_bp.route('/jobs/<int:job_id>/status/<string:new_status>', methods=['POST'])
@employer_required
def toggle_job_status(job_id, new_status):
    job = Job.query.filter_by(id=job_id, employer_id=current_user.id).first_or_404()
    if new_status in ['active', 'closed', 'draft']:
        job.status = new_status
        db.session.commit()
        flash(f'Job status updated to {new_status.title()}.', 'info')
    return redirect(url_for('employer.manage_jobs'))


@employer_bp.route('/jobs/<int:job_id>/delete', methods=['POST'])
@employer_required
def delete_job(job_id):
    job = Job.query.filter_by(id=job_id, employer_id=current_user.id).first_or_404()
    title = job.title
    db.session.delete(job)
    db.session.commit()
    flash(f'Job listing "{title}" and all associated applications have been deleted.', 'warning')
    return redirect(url_for('employer.manage_jobs'))


@employer_bp.route('/applicants')
@employer_bp.route('/applicants/<int:job_id>')
@employer_required
def applicants(job_id=None):
    employer_jobs = current_user.posted_jobs.all()
    job_ids = [j.id for j in employer_jobs]

    selected_job = None
    if job_id:
        selected_job = Job.query.filter_by(id=job_id, employer_id=current_user.id).first_or_404()
        query = Application.query.filter_by(job_id=job_id)
    else:
        query = Application.query.filter(Application.job_id.in_(job_ids)) if job_ids else None

    status_filter = request.args.get('status')
    if query and status_filter:
        query = query.filter(Application.status == status_filter)

    applications = query.order_by(Application.applied_at.desc()).all() if query else []

    return render_template(
        'employer/applicants.html',
        applications=applications,
        employer_jobs=employer_jobs,
        selected_job=selected_job,
        current_status=status_filter
    )


@employer_bp.route('/applications/<int:app_id>/status', methods=['POST'])
@employer_required
def update_application_status(app_id):
    application = Application.query.get_or_404(app_id)
    # Check that current employer owns the job
    if application.job.employer_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('employer.dashboard'))

    new_status = request.form.get('status')
    valid_statuses = ['Pending', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted']
    
    if new_status in valid_statuses:
        application.status = new_status
        application.reviewed_at = datetime.utcnow()
        db.session.commit()
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'status': new_status})
            
        flash(f'Candidate application marked as {new_status}.', 'success')

    return redirect(request.referrer or url_for('employer.applicants'))


@employer_bp.route('/company-profile', methods=['GET', 'POST'])
@employer_required
def company_profile():
    company = current_user.company_profile
    if not company:
        company = CompanyProfile(user_id=current_user.id, company_name='My Company')
        db.session.add(company)
        db.session.commit()

    form = CompanyProfileForm(obj=company)

    if form.validate_on_submit():
        company.company_name = form.company_name.data.strip()
        company.tagline = form.tagline.data.strip() if form.tagline.data else None
        company.industry = form.industry.data.strip()
        company.company_size = form.company_size.data
        company.website = form.website.data.strip() if form.website.data else None
        company.location = form.location.data.strip() if form.location.data else None
        company.founded_year = form.founded_year.data
        company.about = form.about.data

        if form.logo.data:
            logo_filename = save_uploaded_file(
                form.logo.data,
                current_app.config['LOGO_FOLDER'],
                current_app.config['ALLOWED_IMAGE_EXTENSIONS']
            )
            if logo_filename:
                company.logo_filename = logo_filename

        db.session.commit()
        flash('Company profile details saved successfully!', 'success')
        return redirect(url_for('employer.company_profile'))

    return render_template('employer/company_profile.html', form=form, company=company)
