from flask import Blueprint, render_template, request, session, redirect, url_for
from db import mysql  # Importa mysql desde db.py

views = Blueprint("views", __name__)

@views.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM puesto WHERE estado = 'activo'")
    puestos_activos = cur.fetchall()

    cur.execute("SELECT * FROM puesto WHERE estado = 'inactivo'")
    puestos_inactivos = cur.fetchall()

    cur.close()

    return render_template("index.html", puestos_activos=puestos_activos, puestos_inactivos=puestos_inactivos)

@views.route('/add', methods=['POST'])
def add_puesto():
    title = request.form.get('title')
    price = request.form.get('price')
    image_url = request.form.get('image_url')
    return render_template('index.html', title=title, price=price, image_url=image_url)

@views.route("/usuario", methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        user = request.form['user']
        clave = request.form['clave']
        nombre = request.form['nombre']
        wsp = request.form['wsp']
        datos = request.form['datos bancarios']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (usuario, clave, nombre, wsp, datos) VALUES (%s, %s, %s, %s, %s)", (user, clave, nombre, wsp, datos))
        mysql.connection.commit()
        cur.close()
        return "success"
    return render_template("usuario.html")

@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        
        username = request.form['username']
        password = request.form['clave']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuario WHERE usuario = %s AND clave = %s', (username, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('views.home'))
        
        return 'Usuario o clave incorrecta', 401
    
    return render_template("login.html")
@views.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('views.home'))

@views.route("/puesto", methods=['GET', 'POST'])
def agregar_puesto():
    if request.method == 'POST':
        if 'username' in session:
            usuario_id = session['user_id'] 
            titulo = request.form['titulo']
            productos = request.form['productos']
            ofertas = request.form.get('ofertas', '') 
            estado = 'inactivo'  
            
            
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                
            
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO puesto (id, titulo, productos, ofertas, estado) VALUES (%s, %s, %s, %s, %s)",
                        (usuario_id, titulo, productos, ofertas, estado))
            mysql.connection.commit()
            cur.close()
            
            return "Puesto creado correctamente."
        else:
            return "Debe iniciar sesión para crear un puesto."
    
    return render_template("puesto.html")