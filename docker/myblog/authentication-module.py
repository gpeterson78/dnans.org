# app/__init__.py
import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
app.config['HUGO_SITE_PATH'] = os.environ.get('HUGO_SITE_PATH', '/shared/generated')
app.config['CONTENT_PATH'] = os.environ.get('CONTENT_PATH', '/shared/content')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', '/shared/uploads')

# Initialize extensions
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
ckeditor = CKEditor(app)

# Setup admin
from app.admin import configure_admin
admin = Admin(app, name='Blog Admin', template_mode='bootstrap4')
configure_admin(admin)

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)

from app.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return redirect(url_for('admin.index'))

@app.route('/internal/<path:path>')
def internal_content(path):
    # This route serves internal content that requires authentication
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Here you would serve the protected content
    # This could be from a special folder in Hugo or directly served
    return f"Protected content: {path}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')