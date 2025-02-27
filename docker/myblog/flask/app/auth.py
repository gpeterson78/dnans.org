# app/auth.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Simple user model - in production you'd want a database
class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

# In-memory user store - replace with database in production
users = {
    '1': User('1', 'admin', generate_password_hash('admin_password'), True),
    '2': User('2', 'user', generate_password_hash('user_password'), False)
}

# Configure login manager
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find user by username
        user = next((u for u in users.values() if u.username == form.username.data), None)
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next', url_for('index'))
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))