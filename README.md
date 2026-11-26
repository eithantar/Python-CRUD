# Student Registration System (Flask + MySQL)

A minimal, production-ready CRUD app for registering students using Flask, MySQL, HTML, CSS, and JavaScript.

## Features
- List, search, create, update, and delete students
- Server-side validation and flash messages
- Clean, responsive UI with dark mode (no external CSS framework)
- Docker Compose setup (app + MySQL, table created automatically)

## Requirements
- Python 3.9+
- MySQL 8+

## Setup

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# 4) Create database & table
# Option A: Run the SQL directly in MySQL client
mysql -u root -p < schema.sql

# Option B: Paste the content of schema.sql into your MySQL GUI

# 5) Run the app
python app.py
# App will run on http://127.0.0.1:5000
```

## Running with Docker
```bash
docker compose up --build
# App: http://127.0.0.1:5000
```
`schema.sql` runs automatically the first time the MySQL volume is created.
If you created the volume before, reset it with `docker compose down -v`.

## Environment Variables (`.env`)
```
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET=change-this-secret
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=student_db
```

## Project Structure
```
student_crud_flask/
├── app.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── schema.sql
├── templates/
│   ├── base.html
│   ├── students_list.html
│   └── student_form.html
└── static/
    ├── style.css
    └── app.js
```

## Notes
- Email is unique; attempting to add a duplicate will show an error.
- To use a different DB name, update `.env` and `schema.sql` consistently.
- For production, set a strong `FLASK_SECRET` and place the app behind a real web server (e.g., nginx + gunicorn).

## License
MIT
