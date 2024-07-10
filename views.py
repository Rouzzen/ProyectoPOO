from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db import mysql  # Importa mysql desde db.py
from werkzeug.utils import secure_filename
from flask import current_app
import os
from puesto import Puesto
from usuario import Usuario

views = Blueprint("views", __name__)

def check_user_has_puesto():
    user_id = session.get('user_id')
    if user_id:
        return Puesto.get_by_id(mysql, user_id) is not None
    return False

@views.route("/")
def home():
    puestos_activos = Puesto.get_all_puestos_by_estado(mysql, 'activo')
    puestos_inactivos = Puesto.get_all_puestos_by_estado(mysql, 'inactivo')
    usuarios = Usuario.get_all(mysql)
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

        usuario = Usuario(None, user, clave, nombre, wsp, datos)
        usuario.save_to_db(mysql)

        flash('Cuenta creada con éxito')
        return redirect(url_for('views.login'))
    return render_template("usuario.html", user_has_puesto=check_user_has_puesto())

@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        
        username = request.form['username']
        password = request.form['clave']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE usuario = %s AND clave = %s', (username, password))
        user = cur.fetchone()
        
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
        
        puesto = Puesto(usuario_id, titulo, productos, ofertas, imagen_path, estado)
        puesto.save_to_db(mysql)
        
        return redirect(url_for('views.home'))
    
    return render_template("puesto.html", user_has_puesto=check_user_has_puesto())

@views.route("/ver_puesto")
def ver_puesto():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    user_id = session['user_id']
    puesto = Puesto.get_by_id(mysql, user_id)

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

    puesto = Puesto.get_by_id(mysql, puesto_id)
    if puesto:
        puesto.titulo = titulo
        puesto.productos = productos
        puesto.ofertas = ofertas
        if imagen_path:
            puesto.imagen = imagen_path
        puesto.update_in_db(mysql)

    return redirect(url_for('views.ver_puesto'))

@views.route("/toggle_estado/<int:puesto_id>", methods=['POST'])
def toggle_estado(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    puesto = Puesto.get_by_id(mysql, puesto_id)
    if puesto:
        puesto.estado = 'inactivo' if puesto.estado == 'activo' else 'activo'
        puesto.update_in_db(mysql)

    return redirect(url_for('views.ver_puesto'))

@views.route("/borrar_puesto/<int:puesto_id>", methods=['POST'])
def borrar_puesto(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM puesto WHERE id_p = %s", (puesto_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('views.home'))

@views.route("/ver_perfil", methods=['GET', 'POST'])
def ver_perfil():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    
    user_id = session['user_id']
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        wsp = request.form['wsp']
        datos = request.form['datos']
        
        usuario = Usuario.get_by_id(mysql, user_id)
        if usuario:
            usuario.nombre = nombre
            usuario.wsp = wsp
            usuario.datos = datos
            usuario.update_in_db(mysql)
        
        return redirect(url_for('views.ver_perfil'))
    
    usuario = Usuario.get_by_id(mysql, user_id)
    
    return render_template("ver_perfil.html", usuario=usuario, user_has_puesto=check_user_has_puesto())
