from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")  # Habilita las restricciones de clave foránea
    return conn

def get_user_info(user_id):
    # Obtén la información del usuario de la base de datos
    conny = get_db_connection()
    db = conny.cursor()
    user = db.execute("SELECT * FROM doctors WHERE id = ?", (user_id,)).fetchone()
    conny.close()

    # Si el usuario no existe, devuelve None
    if user is None:
        return None

    return user

def get_patients(user_id):
    try:
        conny = get_db_connection()
        db = conny.cursor()
        patients = db.execute("SELECT * FROM patients WHERE doctor_id = ?", (user_id,)).fetchall()
        conny.close()
        patients = [dict(patient) for patient in patients]
        return patients
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return None
    


def get_jobs(patient_id):
    try:
        conny = get_db_connection()
        db = conny.cursor()
        jobs = db.execute("SELECT * FROM jobs WHERE patient_id = ?", (patient_id,)).fetchall()
        conny.close()
        jobs = [dict(job) for job in jobs]
        return jobs
    except Exception as e:
        print(f"Error al obtener trabajos: {e}")
    return None

def get_files_by_job_id(job_id):
    # Aquí deberías implementar la lógica para obtener los archivos de la base de datos
    # basado en el job_id. Este es un ejemplo de cómo podría verse la función.
    try:
        conn = get_db_connection()
        db = conn.cursor()
        db.execute('SELECT * FROM job_uploads JOIN uploads ON job_uploads.upload_id = uploads.id WHERE job_uploads.job_id = ?', (job_id,))
        files = db.fetchall()
        conn.close()
        return files
    except Exception as e:
        print(f"Error al obtener archivos: {e}")
    return None

def get_job(job_id):
    try:
        conn = get_db_connection()
        db = conn.cursor()
        job = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        conn.close()
        return job
    except Exception as e:
        print(f"Error al obtener trabajo: {e}")
    return None