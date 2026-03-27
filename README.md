# Notes Sharing Platform

A full-stack web application built with Python and Flask that allows users to create, share, and view notes. Developed with a focus on clean code, responsive design, and security.

## Features
- **User Authentication**: Secure signup and login using hashed passwords.
- **CRUD Operations**: Create, Read, Update, and Delete your personal notes.
- **Public vs Private Notes**: Choose whether to make your notes visible to the world or keep them to yourself.
- **Markdown Support**: Style your notes easily using Markdown. They will be rendered beautifully when viewed.
- **Search & Pagination**: Easily discover public notes via the exploration feed, complete with search and paginated results.
- **RESTful API**: External endpoints to interact with the notes programmatically.

## Tech Stack
- **Backend**: Python 3, Flask
- **Database**: SQLite, Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Utilities**: Werkzeug Security, Flask-Login, Markdown

## Project Structure
- `app.py`: Main application factory and initialization.
- `models/`: Database models for User and Note.
- `routes/`: Flask blueprints for grouping auth, notes, and api logic securely.
- `templates/`: Jinja2 UI templates using Bootstrap.
- `static/`: Custom CSS styling.

## Local Setup Instructions

1. **Prerequisites**
   Ensure you have Python 3 installed.
   
2. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd "Notes Sharing Platform"
   ```

3. **Initialize the Virtual Environment & Install Dependencies**
   If you haven't already:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   The database tables are automatically generated on the first run.

5. **Access the App**
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints (`/api`)
- `GET /api/notes`: Fetch all public notes (or user's specific notes).
- `GET /api/notes/<id>`: Retrieve a specific note by ID.
- `POST /api/notes`: Create a new note (requires authentication cookie).
