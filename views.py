from flask import Blueprint, render_template, request, session, redirect, url_for
from db import mysql  # Importa mysql desde db.py
from werkzeug.utils import secure_filename
from flask import redirect, url_for
from flask import current_app
import os

views = Blueprint("views", __name__)

@views.route("/")
def home():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM puesto WHERE estado = 'activo'")
    puestos_activos = cur.fetchall()

    cur.execute("SELECT * FROM puesto WHERE estado = 'inactivo'")
    puestos_inactivos = cur.fetchall()
    
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()

    user_id = session.get('user_id')
    user_has_puesto = False

    if user_id:
        cur.execute("SELECT 1 FROM puesto WHERE id_p = %s LIMIT 1", (user_id,))
        user_has_puesto = cur.fetchone() is not None

    cur.close()
    return render_template("index.html", puestos_activos=puestos_activos, puestos_inactivos=puestos_inactivos, usuarios=usuarios, user_has_puesto=user_has_puesto)

@views.route("/usuario", methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        user = request.form['user']
        clave = request.form['clave']
        nombre = request.form['nombre']
        wsp = request.form['wsp']
        datos = request.form['datos bancarios']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (usuario, clave, nombre, wsp, datos) VALUES (%s, %s, %s, %s, %s)", 
                    (user, clave, nombre, wsp, datos))
        mysql.connection.commit()
        cur.close()
        
        # Redirigir al home después de crear el usuario
        return redirect(url_for('views.home'))
    
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
        if 'user_id' in session:
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
            
            # Redirigir al home después de crear el puesto
            return redirect(url_for('views.home'))
        else:
            return "Debe iniciar sesión para crear un puesto."
    
    return render_template("puesto.html")

@views.route("/ver_puesto")
def ver_puesto():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM puesto WHERE id_p = %s", (user_id,))
    puesto = cur.fetchone()

    cur.close()
    return render_template("ver_puesto.html", puesto=puesto)


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

    cur = mysql.connection.cursor()
    if imagen_path:
        cur.execute("""
            UPDATE puesto 
            SET titulo = %s, productos = %s, ofertas = %s, imagen = %s
            WHERE id_p = %s
        """, (titulo, productos, ofertas, imagen_path, puesto_id))
    else:
        cur.execute("""
            UPDATE puesto 
            SET titulo = %s, productos = %s, ofertas = %s
            WHERE id_p = %s
        """, (titulo, productos, ofertas, puesto_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('views.ver_puesto'))


@views.route("/toggle_estado/<int:puesto_id>", methods=['POST'])
def toggle_estado(puesto_id):
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT estado FROM puesto WHERE id_p = %s", (puesto_id,))
    estado_actual = cur.fetchone()[0]

    nuevo_estado = 'inactivo' if estado_actual == 'activo' else 'activo'
    cur.execute("UPDATE puesto SET estado = %s WHERE id_p = %s", (nuevo_estado, puesto_id))
    mysql.connection.commit()
    cur.close()

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
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET nombre=%s, wsp=%s, datos=%s WHERE id=%s", (nombre, wsp, datos, user_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('views.ver_perfil'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
    usuario = cur.fetchone()
    cur.close()
    
    return render_template("ver_perfil.html", usuario=usuario)