from flask import Flask
from views import views
import os
from db import mysql
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "proyecto"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql.init_app(app)

app.register_blueprint(views, url_prefix="/views")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/views")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, port=8000)
