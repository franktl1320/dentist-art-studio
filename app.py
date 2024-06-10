import os
from helpers import apology, login_required, get_db_connection, get_user_info, get_patients, get_jobs
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session





app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Configuración de Flask-Session
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    user = session.get("user_info")
    jobs = {}
    if user is not None:
        patients = get_patients(session.get("user_id"))

        # check for empty list
        if patients:
            #gets the jobs for each patient
            for patient in patients:
                job = get_jobs(patient['id'])
                jobs[patient['id']] = job
    else:
        patients = []
    return render_template('index.html', user=user, patients=patients, jobs=jobs) 


@app.route('/comanda', methods=('GET','POST'))
@login_required
def comanda():
    user = session["user_info"]
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
            flash("Debe proporcionar un nombre de usuario")
            return redirect(url_for('login'))
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Debe proporcionar una contraseña")
            return redirect(url_for('login'))
        
        # Query database for username
        db = get_db_connection()

        rows = db.execute("SELECT * FROM user WHERE username =?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        user = get_user_info(session["user_id"])
        user_info = dict(user)
        session["user_info"] = user_info
        
        
        flash('Login successful!')  # Aquí mostramos el mensaje flash
        return redirect(url_for('index'))
        

    #Via GET
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""
    user = session.get("user_info")
    # Forget any user_id

    session.clear()

    # Flash a goodbye message
    flash(f"Hasta luego,  Dr. {user['last_name']}!")

    # Redirect user to login form
    return redirect(url_for('index'))


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
            return redirect(url_for('index'))
        except (KeyError, TypeError, ValueError):
            return apology("invalid username")

    # via GET #
    return render_template("register.html")


@app.route('/add_patient', methods=('GET','POST'))
@login_required
def add_patient():
    GUM_COLOR_OPTIONS = ['ND1', 'ND2', 'ND3', 'ND4', 'ND5', 'ND6', 'ND7', 'ND8', 'ND9']
    COLORIMETER_OPTIONS = ['A1', 'A2', 'A3', 'A3.5', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'D2', 'D3', 'D4']
    if request.method == 'POST':
        # Aquí va el código para manejar el formulario de agregar paciente
        #Ensure name was submitted
        if not request.form.get('first_name'):
            flash("Debe proporcionar un nombre")
            return redirect(url_for('add_patient'))
            
        first_name = request.form['first_name']

        if not request.form.get('last_name'):
            flash("Debe proporcionar un apellido")
            return redirect(url_for('add_patient'))
        last_name = request.form['last_name']

        #ensure age was submitted
        if not request.form.get('age'):
            flash("Debe proporcionar una edad")
            return redirect(url_for('add_patient'))
        age = request.form['age']       
        face_shape = request.form.get('face_shape')
        basic_color = request.form.get('basic_color')  # Estos campos pueden ser None, así que usamos .get
        colorimeter = request.form.get('colorimeter')
        gum_color = request.form.get('gum_color')
        doctor_id = session['user_id']  # Asumiendo que el id del doctor está en la sesión

        try:
            conn = get_db_connection()
            db = conn.cursor()
            db.execute(
                'INSERT INTO patients (first_name, last_name, age, face_shape, basic_color, colorimeter, gum_color, doctor_id) VALUES (?,?,?, ?, ?, ?, ?, ?)',
                (first_name, last_name, age, face_shape, basic_color, colorimeter, gum_color, doctor_id)
            )
            conn.commit()
            conn.close()

            flash('Paciente agregado exitosamente!')
            return redirect(url_for('index'))
        except Exception as e:
            return apology("Ocurrió un error al agregar el paciente: " + str(e))
    else:
        # Si el método es GET, mostramos el formulario de agregar paciente
        return render_template('add_patient.html', colorimeter_options=COLORIMETER_OPTIONS, gum_color_options=GUM_COLOR_OPTIONS)


@app.route('/add_job/<int:patient_id>', methods=('GET','POST'))
@login_required
def add_job(patient_id):
    JOB_TYPE_LIST = ['Corona', 'Carilla', 'Incrustación', 'Encerado']
    JOB_MATERIAL_LIST =['Metal-Cerámica', 'E-Max', 'Zirconia', 'Ceromero', 'P.M.M.A.']
    patients = get_patients(session.get("user_id"))
    patient = next((patient for patient in patients if patient['id'] == patient_id), None) 
    # Verificar si el paciente es "falsy"
    if not patient:
        flash('El paciente no existe o no es válido')
        return redirect(url_for('index'))
    if request.method == 'POST':
        teeth = request.form.getlist('teeth')
        if not teeth:
            flash('Debe seleccionar al menos un diente')
            return redirect(url_for('add_job', patient_id=patient_id))
        teeth_string = ', '.join(teeth)

        comments = request.form.get('comments')
        tooth_type = request.form.get('tooth_type')
        job_type = request.form.get('job_type')
        job_material = request.form.get('job_material')
        job_option = request.form.get('job_option')
        status = f'Recibido'
        try:
            conn = get_db_connection()
            db = conn.cursor()
            db.execute(
                'INSERT INTO jobs (teeth, patient_id,comments, tooth_type, job_type, job_material, job_option, status ) VALUES (?,?,?,?,?,?,?,?)',
                (teeth_string, patient_id, comments, tooth_type, job_type, job_material,job_option, status)
            )
            conn.commit()
            conn.close()
            flash('Trabajo agregado exitosamente!')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Ocurrio un eror: {e}")
            return apology("Ocurrió un error al agregar el trabajo")
    return render_template('add_job.html', patient=patient, job_type_list=JOB_TYPE_LIST, job_material_list=JOB_MATERIAL_LIST)