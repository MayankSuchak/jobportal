from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, User, UserProfile, CompanyProfile
from app.forms import LoginForm, JobSeekerRegisterForm, EmployerRegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_seeker:
            return redirect(url_for('seeker.dashboard'))
        elif current_user.is_employer:
            return redirect(url_for('employer.dashboard'))
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.display_name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            
            if user.is_seeker:
                return redirect(url_for('seeker.dashboard'))
            elif user.is_employer:
                return redirect(url_for('employer.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please check your credentials.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.register_seeker'))


@auth_bp.route('/register/seeker', methods=['GET', 'POST'])
def register_seeker():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = JobSeekerRegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
            role='jobseeker'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        profile = UserProfile(
            user_id=user.id,
            full_name=form.full_name.data.strip()
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash('Account created successfully! Welcome to your candidate dashboard.', 'success')
        return redirect(url_for('seeker.profile'))

    return render_template('auth/register.html', form=form, active_role='seeker')


@auth_bp.route('/register/employer', methods=['GET', 'POST'])
def register_employer():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = EmployerRegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
            role='employer'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        company = CompanyProfile(
            user_id=user.id,
            company_name=form.company_name.data.strip(),
            industry=form.industry.data.strip()
        )
        db.session.add(company)
        db.session.commit()

        login_user(user)
        flash('Employer account created! Complete your company profile to start hiring.', 'success')
        return redirect(url_for('employer.company_profile'))

    return render_template('auth/register.html', form=form, active_role='employer')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
