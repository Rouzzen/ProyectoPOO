from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db import mysql  # Importa mysql desde db.py
from werkzeug.utils import secure_filename
from flask import current_app
import os
from puesto import  Puesto
from usuario import Usuario

views = Blueprint("views", __name__)

def check_user_has_puesto():
    user_id = session.get('user_id')
    if user_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1 FROM puesto WHERE id_p = %s LIMIT 1", (user_id,))
        user_has_puesto = cur.fetchone() is not None
        cur.close()
        return user_has_puesto
    return False

@views.route("/")
def home():
    puestos_activos = []
    puestos_inactivos = []
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_p FROM puesto WHERE estado = 'activo'")
    puestos_activos_ids = cur.fetchall()
    cur.execute("SELECT id_p FROM puesto WHERE estado = 'inactivo'")
    puestos_inactivos_ids = cur.fetchall()
    cur.close()

    for id_p in puestos_activos_ids:
        puesto = Puesto.obtener_por_id(id_p[0], mysql)
        puestos_activos.append(puesto)

    for id_p in puestos_inactivos_ids:
        puesto = Puesto.obtener_por_id(id_p[0], mysql)
        puestos_inactivos.append(puesto)

    # Obtener todos los usuarios
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM usuario")
    usuarios_ids = cur.fetchall()
    cur.close()

    usuarios = [Usuario.obtener_por_id(id_u[0], mysql) for id_u in usuarios_ids]

    user_has_puesto = check_user_has_puesto()

    return render_template("index.html", puestos_activos=puestos_activos, puestos_inactivos=puestos_inactivos, usuarios=usuarios, user_has_puesto=user_has_puesto)


@views.route("/usuario", methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        user = request.form.get('user')
        clave = request.form.get('clave')
        nombre = request.form.get('nombre')
        wsp = request.form.get('wsp')
        datos = request.form.get('datos')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (usuario, clave, nombre, wsp, datos) VALUES (%s, %s, %s, %s, %s)", (user, clave, nombre, wsp, datos))
        mysql.connection.commit()
        cur.close()
        flash('Cuenta creada con éxito')
        return redirect(url_for('views.login'))
    return render_template("usuario.html", user_has_puesto=check_user_has_puesto())

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
    
    return render_template("login.html", user_has_puesto=check_user_has_puesto())

@views.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('views.home'))

@views.route("/puesto", methods=['GET', 'POST'])
def agregar_puesto():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    if check_user_has_puesto():
        flash('Ya tienes un puesto creado.')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        usuario_id = session['user_id']
        titulo = request.form['titulo']
        productos = request.form['productos']
        ofertas = request.form.get('ofertas', '')
        estado = 'inactivo'
        
        imagen_path = None
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                filename = secure_filename(imagen.filename)
                imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                imagen.save(imagen_path)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO puesto (id_p, titulo, productos, ofertas, estado, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
                    (usuario_id, titulo, productos, ofertas, estado, imagen_path))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('views.home'))
    
    return render_template("puesto.html", user_has_puesto=check_user_has_puesto())

@views.route("/ver_puesto")
def ver_puesto():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    user_id = session['user_id']
    usuario = Usuario.obtener_por_id(user_id, mysql)
    puesto = usuario.obtener_puesto(mysql)

    return render_template("ver_puesto.html", puesto=puesto, user_has_puesto=check_user_has_puesto())

@views.route("/editar_puesto/<int:puesto_id>", methods=['POST'])
def editar_puesto(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    titulo = request.form['titulo']
    productos = request.form['productos']
    ofertas = request.form['ofertas']

    imagen_path = None
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            imagen_path = os.path.join('static', filename)

    usuario = Usuario.obtener_por_id(session['user_id'], mysql)
    puesto = usuario.obtener_puesto(mysql)
    puesto.actualizar_detalles(titulo, productos, ofertas, mysql, imagen_path)

    return redirect(url_for('views.ver_puesto'))

@views.route("/toggle_estado/<int:puesto_id>", methods=['POST'])
def toggle_estado(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    usuario = Usuario.obtener_por_id(session['user_id'], mysql)
    puesto = usuario.obtener_puesto(mysql)
    nuevo_estado = 'inactivo' if puesto.estado == 'activo' else 'activo'
    puesto.actualizar_estado(nuevo_estado, mysql)

    return redirect(url_for('views.ver_puesto'))

@views.route("/borrar_puesto/<int:puesto_id>", methods=['POST'])
def borrar_puesto(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    usuario = Usuario.obtener_por_id(session['user_id'], mysql)
    puesto = usuario.obtener_puesto(mysql)
    puesto.eliminar(mysql)

    return redirect(url_for('views.home'))

@views.route("/ver_perfil", methods=['GET', 'POST'])
def ver_perfil():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    
    user_id = session['user_id']
    usuario = Usuario.obtener_por_id(user_id, mysql)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        wsp = request.form['wsp']
        datos = request.form['datos']
        usuario.actualizar_perfil(nombre, wsp, datos, mysql)
        
        return redirect(url_for('views.ver_perfil'))

    return render_template("ver_perfil.html", usuario=usuario, user_has_puesto=check_user_has_puesto())
