import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db, seeker_required
from app.models import UserProfile, Job, Application, SavedJob
from app.forms import JobSeekerProfileForm, ApplicationForm

seeker_bp = Blueprint('seeker', __name__)

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


@seeker_bp.route('/dashboard')
@seeker_required
def dashboard():
    profile = current_user.seeker_profile
    applications = current_user.applications.order_by(Application.applied_at.desc()).all()
    saved_jobs = current_user.saved_jobs.order_by(SavedJob.created_at.desc()).all()

    # Calculate metrics
    total_applications = len(applications)
    shortlisted_count = sum(1 for a in applications if a.status == 'Shortlisted')
    pending_count = sum(1 for a in applications if a.status == 'Pending')
    accepted_count = sum(1 for a in applications if a.status == 'Accepted')

    # Recommended jobs based on candidate skills
    recommended_jobs = []
    if profile and profile.skills:
        skills = [s.strip().lower() for s in profile.skills.split(',') if s.strip()]
        if skills:
            from sqlalchemy import or_
            conditions = [Job.skills_required.ilike(f"%{s}%") for s in skills]
            recommended_jobs = Job.query.filter(
                Job.status == 'active',
                or_(*conditions)
            ).order_by(Job.created_at.desc()).limit(4).all()

    if not recommended_jobs:
        recommended_jobs = Job.query.filter_by(status='active').order_by(Job.created_at.desc()).limit(4).all()

    return render_template(
        'seeker/dashboard.html',
        profile=profile,
        applications=applications[:5],
        total_applications=total_applications,
        shortlisted_count=shortlisted_count,
        pending_count=pending_count,
        accepted_count=accepted_count,
        saved_jobs_count=len(saved_jobs),
        recommended_jobs=recommended_jobs
    )


@seeker_bp.route('/applications')
@seeker_required
def applications():
    applications_list = current_user.applications.order_by(Application.applied_at.desc()).all()
    return render_template('seeker/applications.html', applications=applications_list)


@seeker_bp.route('/saved-jobs')
@seeker_required
def saved_jobs():
    saved_list = current_user.saved_jobs.order_by(SavedJob.created_at.desc()).all()
    return render_template('seeker/saved_jobs.html', saved_jobs=saved_list)


@seeker_bp.route('/profile', methods=['GET', 'POST'])
@seeker_required
def profile():
    user_profile = current_user.seeker_profile
    if not user_profile:
        user_profile = UserProfile(user_id=current_user.id)
        db.session.add(user_profile)
        db.session.commit()

    form = JobSeekerProfileForm(obj=user_profile)

    if form.validate_on_submit():
        user_profile.full_name = form.full_name.data
        user_profile.headline = form.headline.data
        user_profile.phone = form.phone.data
        user_profile.location = form.location.data
        user_profile.experience_years = form.experience_years.data or 0
        user_profile.education = form.education.data
        user_profile.skills = form.skills.data
        user_profile.bio = form.bio.data
        user_profile.linkedin_url = form.linkedin_url.data
        user_profile.github_url = form.github_url.data
        user_profile.portfolio_url = form.portfolio_url.data

        if form.resume.data:
            filename = save_uploaded_file(
                form.resume.data,
                current_app.config['RESUME_FOLDER'],
                current_app.config['ALLOWED_RESUME_EXTENSIONS']
            )
            if filename:
                user_profile.resume_filename = filename

        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('seeker.profile'))

    return render_template('seeker/profile.html', form=form, profile=user_profile)


@seeker_bp.route('/apply/<int:job_id>', methods=['POST'])
@seeker_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if job.status != 'active':
        flash('This job posting is no longer active.', 'warning')
        return redirect(url_for('main.job_detail', job_id=job.id))

    if current_user.has_applied_to(job.id):
        flash('You have already submitted an application for this position.', 'info')
        return redirect(url_for('main.job_detail', job_id=job.id))

    form = ApplicationForm()
    
    # Determine resume file
    resume_file = None
    if form.resume.data:
        resume_file = save_uploaded_file(
            form.resume.data,
            current_app.config['RESUME_FOLDER'],
            current_app.config['ALLOWED_RESUME_EXTENSIONS']
        )
    elif form.use_profile_resume.data and current_user.seeker_profile and current_user.seeker_profile.resume_filename:
        resume_file = current_user.seeker_profile.resume_filename

    if not resume_file:
        flash('Please upload a resume or add a resume to your profile before applying.', 'danger')
        return redirect(url_for('main.job_detail', job_id=job.id))

    application = Application(
        job_id=job.id,
        seeker_id=current_user.id,
        cover_note=form.cover_note.data,
        resume_filename=resume_file,
        status='Pending'
    )
    db.session.add(application)
    db.session.commit()

    flash(f'Application successfully submitted for {job.title} at {job.employer.company_profile.company_name}!', 'success')
    return redirect(url_for('seeker.applications'))


@seeker_bp.route('/save-toggle/<int:job_id>', methods=['POST'])
@seeker_required
def toggle_save_job(job_id):
    job = Job.query.get_or_404(job_id)
    saved = SavedJob.query.filter_by(seeker_id=current_user.id, job_id=job.id).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        is_saved = False
        message = 'Job removed from saved list.'
    else:
        new_save = SavedJob(seeker_id=current_user.id, job_id=job.id)
        db.session.add(new_save)
        db.session.commit()
        is_saved = True
        message = 'Job saved to your bookmarks!'

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'is_saved': is_saved, 'message': message})

    flash(message, 'info')
    return redirect(request.referrer or url_for('main.job_detail', job_id=job.id))


@seeker_bp.route('/resumes/<filename>')
@login_required
def download_resume(filename):
    # Ensure only owner or recruiter can download
    return send_from_directory(current_app.config['RESUME_FOLDER'], filename, as_attachment=True)
