from flask import Blueprint, jsonify, request
from models import db
from models.note import Note
from models.user import User
from flask_login import login_required, current_user

api_bp = Blueprint('api', __name__)

@api_bp.route('/notes', methods=['GET'])
def get_notes():
    # Returns public notes or user's specific notes if authenticated and requested
    notes_to_fetch = Note.query.filter_by(is_public=True).all()
    results = [
        {
            "id": n.id,
            "title": n.title,
            "author": n.author.username,
            "timestamp": n.timestamp,
        } for n in notes_to_fetch
    ]
    return jsonify({"notes": results})

@api_bp.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get_or_404(id)
    if not note.is_public and (not current_user.is_authenticated or current_user.id != note.author_id):
        return jsonify({"error": "Unauthorized"}), 403
        
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "author": note.author.username,
        "timestamp": note.timestamp,
        "is_public": note.is_public
    })
    
@api_bp.route('/notes', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    if not data or not 'title' in data or not 'content' in data:
        return jsonify({"error": "Bad Request, missing title or content"}), 400
        
    note = Note(
        title=data['title'],
        content=data['content'],
        is_public=data.get('is_public', False),
        author_id=current_user.id
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note created", "id": note.id}), 201
