import sqlite3
from helpers import apology, login_required, get_db_connection, get_user_info
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash






app = Flask(__name__)
app.config['SECRET_KEY'] = 'llavesecreta'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/comanda', methods=('GET','POST'))
@login_required
def comanda():
    user = get_user_info(session["user_id"])
    if request.method == 'POST':
        doctor = request.form['doctor']
        paciente = request.form['paciente']
        return render_template('salida.html', doctor=doctor, paciente=paciente)
    return render_template('comanda.html', user=user)

@app.route('/login', methods=('GET','POST'))
def login():
    #Forget any user
    session.clear()

    #Via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        # Query database for username
        db = get_db_connection()

        rows = db.execute("SELECT * FROM user WHERE username =?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
       
        
        flash('Login successful!')  # Aquí mostramos el mensaje flash
        return redirect("/")
        

    #Via GET
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id

    session.clear()

    # Flash a goodbye message
    flash(f"Hasta luego,  {user_name}!")

    # Redirect user to login form
    return redirect("/")


@app.route('/register', methods=('GET','POST'))
def register():
    #  via POST #
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")
        
        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must provide password confirmation")
        
        # Ensure confirmation and password matches
        if not request.form.get("confirmation") == request.form.get("password"):
            return apology("confirmation password doesnt match")
        
        try:
            conny = get_db_connection()
            db = conny.cursor()
            db.execute("INSERT INTO user (username, hash) VALUES(?,?)",
                       (request.form.get("username"), generate_password_hash(request.form.get("password"))))
            user_id = db.lastrowid  # Aquí obtenemos el ID del usuario recién insertado
            conny.commit()

            # Ahora puedes usar user_id para insertar un nuevo doctor en la tabla doctors
            db.execute("INSERT INTO doctors (user_id, last_name, first_name, e_mail) VALUES(?,?,?,?)",
               (user_id, request.form.get("firstname"), request.form.get("lastname"), request.form.get("email")))
            conny.commit()
            conny.close()

            flash('Registration successful!')  # Aquí mostramos el mensaje flash
            return redirect("/")
        except (KeyError, TypeError, ValueError):
            return apology("invalid username")

    # via GET #
    return render_template("register.html")


