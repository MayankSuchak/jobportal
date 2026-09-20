import os
from functools import wraps
from flask import Flask, abort, flash, redirect, url_for
from flask_login import LoginManager, current_user
from app.models import db, User
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def seeker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_seeker:
            flash('Access restricted to Job Seekers only.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def employer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_employer:
            flash('Access restricted to Employers / Recruiters only.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESUME_FOLDER'], exist_ok=True)
    os.makedirs(app.config['LOGO_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AVATAR_FOLDER'], exist_ok=True)

    # Register custom template filters & helpers
    @app.template_filter('timeago')
    def timeago_filter(dt):
        if not dt:
            return ''
        from datetime import datetime
        now = datetime.utcnow()
        diff = now - dt
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return 'Just now'
        elif seconds < 3600:
            mins = int(seconds // 60)
            return f"{mins}m ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h ago"
        elif seconds < 604800:
            days = int(seconds // 86400)
            return f"{days}d ago"
        else:
            return dt.strftime('%b %d, %Y')

    @app.template_filter('status_badge')
    def status_badge_filter(status):
        mapping = {
            'Pending': 'bg-warning text-dark',
            'Reviewed': 'bg-info text-dark',
            'Shortlisted': 'bg-primary text-white',
            'Accepted': 'bg-success text-white',
            'Rejected': 'bg-danger text-white',
            'active': 'bg-success text-white',
            'closed': 'bg-secondary text-white',
            'draft': 'bg-warning text-dark'
        }
        return mapping.get(status, 'bg-secondary text-white')

    @app.context_processor
    def inject_global_vars():
        from app.models import JobCategory
        categories = JobCategory.query.all()
        return dict(global_categories=categories)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.seeker import seeker_bp
    from app.routes.employer import employer_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(seeker_bp, url_prefix='/seeker')
    app.register_blueprint(employer_bp, url_prefix='/employer')

    with app.app_context():
        db.create_all()

    return app

# Expose default app instance for WSGI servers like Gunicorn (gunicorn app:app)
app = create_app()

