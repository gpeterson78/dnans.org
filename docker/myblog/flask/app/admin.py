# app/admin.py
import os
import subprocess
from flask import flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user
from flask_ckeditor import CKEditorField
from wtforms import TextAreaField, SelectField
import markdown
import frontmatter
import datetime
import uuid

class AuthenticatedView:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=url_for(name, **kwargs)))

class ContentEditor(AuthenticatedView, BaseView):
    @expose('/')
    def index(self):
        content_path = current_app.config['CONTENT_PATH']
        posts = []
        
        # List existing content
        for root, dirs, files in os.walk(content_path):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        post = frontmatter.load(f)
                        post_data = {
                            'title': post.get('title', 'Untitled'),
                            'date': post.get('date', 'Unknown'),
                            'draft': post.get('draft', True),
                            'path': os.path.relpath(filepath, content_path),
                            'visibility': post.get('visibility', 'public')
                        }
                        posts.append(post_data)
                        
        return self.render('admin/content_list.html', posts=posts)
    
    @expose('/new', methods=['GET', 'POST'])
    def new_post(self):
        if request.method == 'POST':
            title = request.form.get('title', 'Untitled')
            content = request.form.get('content', '')
            visibility = request.form.get('visibility', 'public')
            
            # Create slug from title
            slug = '-'.join(title.lower().split())
            
            # Create post with frontmatter
            post = frontmatter.Post(content)
            post['title'] = title
            post['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            post['draft'] = False
            post['slug'] = slug
            post['visibility'] = visibility
            
            # Save to file
            content_path = current_app.config['CONTENT_PATH']
            directory = os.path.join(content_path, 'posts')
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, f"{slug}.md")
            with open(filepath, 'w') as f:
                f.write(frontmatter.dumps(post))
            
            # Trigger Hugo build
            self.trigger_hugo_build()
            
            flash('Post created successfully!')
            return redirect(url_for('.index'))
        
        return self.render('admin/content_edit.html')
    
    @expose('/edit/<path:filepath>', methods=['GET', 'POST'])
    def edit_post(self, filepath):
        content_path = current_app.config['CONTENT_PATH']
        full_path = os.path.join(content_path, filepath)
        
        if request.method == 'POST':
            title = request.form.get('title', 'Untitled')
            content = request.form.get('content', '')
            visibility = request.form.get('visibility', 'public')
            
            # Update post with frontmatter
            with open(full_path, 'r') as f:
                post = frontmatter.load(f)
            
            post['title'] = title
            post['visibility'] = visibility
            post.content = content
            
            with open(full_path, 'w') as f:
                f.write(frontmatter.dumps(post))
            
            # Trigger Hugo build
            self.trigger_hugo_build()
            
            flash('Post updated successfully!')
            return redirect(url_for('.index'))
        
        # Load existing post
        with open(full_path, 'r') as f:
            post = frontmatter.load(f)
            
        post_data = {
            'title': post.get('title', 'Untitled'),
            'content': post.content,
            'visibility': post.get('visibility', 'public')
        }
        
        return self.render('admin/content_edit.html', post=post_data)
    
    def trigger_hugo_build(self):
        """Trigger a Hugo build by touching a file or calling the API"""
        # This could be implemented in various ways:
        # 1. Direct shell call to Hugo container
        # 2. Write a trigger file that the Hugo container watches
        # 3. Make an API call to a Hugo webhook
        
        # Simple implementation - create a trigger file
        trigger_file = '/shared/trigger_build'
        with open(trigger_file, 'w') as f:
            f.write(str(datetime.datetime.now()))

class MediaManager(AuthenticatedView, BaseView):
    @expose('/')
    def index(self):
        uploads_path = current_app.config['UPLOAD_FOLDER']
        media_files = []
        
        # List media files
        for root, dirs, files in os.walk(uploads_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.mp4')):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, uploads_path)
                    media_files.append({
                        'name': file,
                        'path': rel_path,
                        'url': f"/uploads/{rel_path}"
                    })
        
        return self.render('admin/media_list.html', media_files=media_files)
    
    @expose('/upload', methods=['POST'])
    def upload(self):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            uploads_path = current_app.config['UPLOAD_FOLDER']
            os.makedirs(uploads_path, exist_ok=True)
            file.save(os.path.join(uploads_path, filename))
            flash('File uploaded successfully')
            
        return redirect(url_for('.index'))

def configure_admin(admin):
    admin.add_view(ContentEditor(name='Content', endpoint='content'))
    admin.add_view(MediaManager(name='Media', endpoint='media'))