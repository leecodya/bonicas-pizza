from flask import Flask, render_template, flash, request, redirect, url_for
from model.database import Database
from model.pizza import Pizza

db = Database()
sizes = ["Medium (12 inches)", "Large (16 inches)", "X-Large (20 inches)", "Party (24 inches)"]
crusts = ["Thin", "Regular", "Deep Dish"]
cheeses = ["Fresh Motz", "Romano", "Feta", "Ricotta", "Shredded Motz", "Cheddar"]
sauces = ["Marinara", "Creamy Garlic", "Basil Pesto", "Creamy Pesto", "Smoked Chipotle", "Southern BBQ", "Garlic Butter"]
toppings = ["Anchovies", "Basil", "Banana Peppers", "Bacon", "Black Olives", "Chicken", "Garlic", "Green Peppers", "Green Olives", "Ham", "Italian Sausage", "Jalapenos", "Mushrooms", "Onion", "Pepperoni", "Pineapple", "Roasted Red Peppers", "Sirloin Steak Tips", "Spinach"]

items_ordered = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyforlab10'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/nutrition")
def nutrition():
    return render_template("nutrition.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/originals")
def originals():
    originals = db.pizzas.get_pizzas(1)
    return render_template("originals.html", originals=originals)

@app.route("/favorites")
def favorites():
    favorites = db.pizzas.get_pizzas(2)
    return render_template("favorites.html", favorites=favorites)

@app.route("/order-form", methods=["POST", "GET"])
def order_form():
    username = request.args.get('username')
    email = request.args.get('email') 
    pizzas = db.pizzas.get_pizzas()
    return render_template("order-form.html", user_name=username, user_email=email, pizzas=pizzas, sizes=sizes, crusts=crusts, cheeses=cheeses, sauces=sauces, toppings=toppings)

@app.route('/add', methods=["POST", "GET"])
def add_to_order():
    username = request.form.get('username')
    email = request.form.get('email')
    size = request.form.get('size')
    crust = request.form.get('crust')
    pizza_id = request.form.get('pizza_id')
    quantity = request.form.get('quantity')

    if not username or not email or not size or not crust or not quantity:
        flash('Missing data. Please check all fields and try again')
        return redirect(url_for('order_form'))

    pizza_id = int(pizza_id)
    quantity = int(quantity)
    pizza = db.pizzas.get_pizza(pizza_id)
    db.order.add_item(pizza_id, pizza.category_id, pizza.name, pizza.description, pizza.price, size, crust, quantity)
    return redirect(url_for('order_confirmation', username=username, email=email))

@app.route('/order-confirmation')
def order_confirmation():
    username = request.args.get('username')
    email = request.args.get('email')
    items = db.order.get_items()
    
    return render_template('order-confirmation.html', items=items, username=username, email=email)

@app.route('/update', methods=["POST"])
def update():
    pizza_id = request.form.get('pizza_id')
    quantity = request.form.get('quantity')
    username = request.form.get('username')
    email = request.form.get('email')

    try:
        quantity = int(quantity)
        db.order.update_item(int(pizza_id), quantity)
        flash("Update successful")
    except ValueError:
        flash("Quantity is not a valid number")

    return redirect(url_for('order_confirmation', username=username, email=email))

@app.route('/delete', methods=["POST"])
def delete():
    pizza_id = request.form.get('pizza_id')
    quantity = 0
    username = request.form.get('username')
    email = request.form.get('email')

    db.order.update_item(int(pizza_id), quantity)
    flash("Deletion successful")

    return redirect(url_for('order_confirmation', username=username, email=email))    

@app.route('/place-order')
def place_order():
    db.order.place_order()
    flash("Your order has been placed")
    return redirect(url_for('order_confirmation'))

@app.route('/<error>')
def not_found(error):
    return render_template("404.html")
