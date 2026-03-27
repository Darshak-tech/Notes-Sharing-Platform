from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db
from models.note import Note
import markdown

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def index():
    # Public Notes with Pagination and Search
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    query = Note.query.filter_by(is_public=True)
    if search_query:
        query = query.filter(Note.title.ilike(f'%{search_query}%') | Note.content.ilike(f'%{search_query}%'))
        
    notes = query.order_by(Note.timestamp.desc()).paginate(page=page, per_page=9, error_out=False)
    
    return render_template('home.html', notes=notes, search_query=search_query)

@notes_bp.route('/dashboard')
@login_required
def dashboard():
    # User's Private Notes
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(author_id=current_user.id).order_by(Note.timestamp.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template('dashboard.html', notes=notes)

@notes_bp.route('/note/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_public = True if request.form.get('is_public') else False
        
        note = Note(title=title, content=content, is_public=is_public, author_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        
        flash('Note created successfully!', 'success')
        return redirect(url_for('notes.dashboard'))
        
    return render_template('create_edit.html', title='Create Note', action='Create')

@notes_bp.route('/note/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)
    if note.author_id != current_user.id:
        abort(403)
        
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.is_public = True if request.form.get('is_public') else False
        db.session.commit()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.dashboard'))
        
    return render_template('create_edit.html', title='Edit Note', action='Edit', note=note)

@notes_bp.route('/note/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if note.author_id != current_user.id:
        abort(403)
        
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'info')
    return redirect(url_for('notes.dashboard'))

@notes_bp.route('/note/<int:id>')
def view(id):
    note = Note.query.get_or_404(id)
    if not note.is_public and (not current_user.is_authenticated or note.author_id != current_user.id):
        abort(403)
        
    # Render markdown content
    rendered_content = markdown.markdown(note.content, extensions=['fenced_code', 'tables'])
    return render_template('view.html', note=note, rendered_content=rendered_content)
