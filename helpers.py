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