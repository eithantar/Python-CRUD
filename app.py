import os
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import connect, Error, errorcode
from dotenv import load_dotenv

load_dotenv()


def is_duplicate_email(err):
    return getattr(err, "errno", None) == errorcode.ER_DUP_ENTRY


def read_student_form():
    return {
        "full_name": request.form.get("full_name", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "phone": request.form.get("phone", "").strip(),
        "major": request.form.get("major", "").strip(),
    }


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET', 'dev-secret')

    print(f"Connecting to DB with host={os.getenv('DB_HOST', 'localhost')}, port={os.getenv('DB_PORT', '3306')}, user={os.getenv('DB_USER', 'root')}, database={os.getenv('DB_NAME', 'student_db')}")

    dbconfig = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("DB_NAME", "student_db"),
        "autocommit": True,
    }

    # Function to create a new database connection
    def get_conn():
        try:
            conn = connect(**dbconfig)
            return conn
        except Error as e:
            raise RuntimeError(f"Failed to create DB connection: {e}")

    @app.route('/')
    def home():
        return redirect(url_for('list_students'))

    @app.route('/students')
    def list_students():
        q = request.args.get('q', '').strip()
        query = "SELECT id, full_name, email, phone, major, created_at FROM students"
        params = ()
        if q:
            query += " WHERE full_name LIKE %s OR email LIKE %s OR phone LIKE %s OR major LIKE %s"
            like = f"%{q}%"
            params = (like, like, like, like)
        query += " ORDER BY created_at DESC, id DESC"

        with get_conn() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, params)
                rows = cur.fetchall()

        return render_template('students_list.html', students=rows, q=q)

    @app.route('/students/new', methods=['GET', 'POST'])
    def create_student():
        form = {}
        if request.method == 'POST':
            form = read_student_form()
            full_name, email, phone, major = form['full_name'], form['email'], form['phone'], form['major']

            if not full_name or not email:
                flash('Full name and email are required.', 'error')
                return render_template('student_form.html', student=None, form=form)

            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO students (full_name, email, phone, major) VALUES (%s, %s, %s, %s)",
                            (full_name, email, phone, major),
                        )
                flash('Student created successfully!', 'success')
                return redirect(url_for('list_students'))
            except Error as e:
                msg = str(e)
                if is_duplicate_email(e):
                    flash('Email already exists.', 'error')
                else:
                    flash(f'Error creating student: {msg}', 'error')

        return render_template('student_form.html', student=None, form=form)

    @app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
    def edit_student(student_id):
        with get_conn() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
                student = cur.fetchone()

        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('list_students'))

        form = student
        if request.method == 'POST':
            form = read_student_form()
            full_name, email, phone, major = form['full_name'], form['email'], form['phone'], form['major']

            if not full_name or not email:
                flash('Full name and email are required.', 'error')
                return render_template('student_form.html', student=student, form=form)

            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE students SET full_name=%s, email=%s, phone=%s, major=%s WHERE id=%s",
                            (full_name, email, phone, major, student_id),
                        )
                flash('Student updated successfully!', 'success')
                return redirect(url_for('list_students'))
            except Error as e:
                msg = str(e)
                if is_duplicate_email(e):
                    flash('Email already exists.', 'error')
                else:
                    flash(f'Error updating student: {msg}', 'error')

        return render_template('student_form.html', student=student, form=form)

    @app.route('/students/<int:student_id>/delete', methods=['POST'])
    def delete_student(student_id):
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
            flash('Student deleted.', 'success')
        except Error as e:
            flash(f'Error deleting student: {e}', 'error')
        return redirect(url_for('list_students'))

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug)