from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route('/add', methods=['POST'])
def add_puesto():
    title = request.form.get('title')
    price = request.form.get('price')
    image_url = request.form.get('image_url')
    return render_template('index.html', title=title, price=price, image_url=image_url)