# app/api.py
from flask import Blueprint, jsonify, request
import json
import os
import datetime

api_bp = Blueprint('api', __name__)

# Simple comment storage - In production use a database
COMMENTS_FILE = '/shared/comments.json'

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_comments(comments):
    os.makedirs(os.path.dirname(COMMENTS_FILE), exist_ok=True)
    with open(COMMENTS_FILE, 'w') as f:
        json.dump(comments, f, indent=2)

@api_bp.route('/comments/<post_slug>', methods=['GET'])
def get_comments(post_slug):
    comments = load_comments()
    post_comments = comments.get(post_slug, [])
    
    # Sort by date, newest first
    post_comments.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Return only public facing fields
    result = []
    for comment in post_comments:
        result.append({
            'author': comment.get('author', 'Anonymous'),
            'message': comment.get('message', ''),
            'date': comment.get('date', '')
        })
    
    return jsonify(result)

@api_bp.route('/comments/<post_slug>', methods=['POST'])
def add_comment(post_slug):
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    comments = load_comments()
    if post_slug not in comments:
        comments[post_slug] = []
    
    new_comment = {
        'author': data.get('author', 'Anonymous'),
        'message': data.get('message'),
        'date': datetime.datetime.now().isoformat(),
        'ip': request.remote_addr
    }
    
    comments[post_slug].append(new_comment)
    save_comments(comments)
    
    return jsonify({'status': 'success', 'comment': {
        'author': new_comment['author'],
        'message': new_comment['message'],
        'date': new_comment['date']
    }})

@api_bp.route('/comments/recent', methods=['GET'])
def recent_comments():
    """Gets the most recent comments across all posts - for your e-paper display"""
    comments = load_comments()
    all_comments = []
    
    # Collect all comments
    for post_slug, post_comments in comments.items():
        for comment in post_comments:
            comment_with_slug = comment.copy()
            comment_with_slug['post'] = post_slug
            all_comments.append(comment_with_slug)
    
    # Sort by date
    all_comments.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Take the 4 most recent
    recent = all_comments[:4]
    
    # Format for the e-paper display
    result = []
    for comment in recent:
        result.append({
            'author': comment.get('author', 'Anonymous'),
            'message': comment.get('message', ''),
            'date': comment.get('date', '')
        })
    
    return jsonify(result)