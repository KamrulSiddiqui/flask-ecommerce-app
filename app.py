from flask import Flask, render_template, session, redirect, url_for, request, flash
from functools import wraps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)


# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
mongo = PyMongo(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('index'))
    return redirect(url_for('signup'))

@app.route('/index')
@login_required
def index():
    products = list(mongo.db.products.find())
    return render_template('index.html', products=products)

@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').lower()
    products = list(mongo.db.products.find({"name": {"$regex": query, "$options": "i"}}))
    return render_template('index.html', products=products)

@app.route('/product/<product_id>')
@login_required
def product_detail(product_id):
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    username = session['user']
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart

    mongo.db.cart_items.insert_one({
        'user': username,
        'product_id': ObjectId(product_id),
        'quantity': cart[product_id],
        'timestamp': datetime.utcnow()
    })

    flash('Product added to cart successfully!', 'cart-success')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = mongo.db.products.find_one({'_id': ObjectId(pid)})
        if product:
            item_total = product['price'] * qty
            total += item_total
            cart_items.append({'product': product, 'quantity': qty, 'total_price': item_total})
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    cart = session.get('cart', {})
    remove_id = request.form.get('remove')
    update_id = request.form.get('update')

    if remove_id and remove_id in cart:
        cart.pop(remove_id)
    elif update_id:
        try:
            qty = int(request.form.get(f'quantity_{update_id}'))
            if qty >= 1:
                cart[update_id] = qty
        except ValueError:
            pass

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty!")
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')

        if not all([name, email, address, payment_method]):
            flash("All fields are required.")
            return redirect(url_for('checkout'))

        cart_items = []
        total = 0
        for pid, qty in cart.items():
            product = mongo.db.products.find_one({'_id': ObjectId(pid)})
            if product:
                item_total = product['price'] * qty
                total += item_total
                cart_items.append({
                    'product_id': product['_id'],
                    'name': product['name'],
                    'quantity': qty,
                    'price': product['price'],
                    'image': product.get('image', '')
                })

        order = {
            'user': session['user'],
            'name': name,
            'email': email,
            'address': address,
            'payment_method': payment_method,
            'items': cart_items,
            'total': total,
            'timestamp': datetime.utcnow()
        }

        mongo.db.orders.insert_one(order)
        session.pop('cart', None)
        flash("Order placed successfully!", "order-success")
        return redirect(url_for('index'))

    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = mongo.db.products.find_one({'_id': ObjectId(pid)})
        if product:
            item_total = product['price'] * qty
            total += item_total
            cart_items.append({'product': product, 'quantity': qty, 'total_price': item_total})

    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/my_orders')
@login_required
def my_orders():
    username = session['user']
    orders = list(mongo.db.orders.find({'user': username}).sort('timestamp', -1))
    return render_template('my_orders.html', orders=orders)

@app.route('/delete_order/<order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    mongo.db.orders.delete_one({'_id': ObjectId(order_id), 'user': session['user']})
    flash("Order deleted successfully!", "order-delete")
    return redirect(url_for('my_orders'))

@app.route('/change_order/<order_id>')
@login_required
def change_order(order_id):
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id), 'user': session['user']})
    if not order:
        flash("Order not found!", "order-error")
        return redirect(url_for('my_orders'))

    cart = {}
    for item in order['items']:
        cart[str(item['product_id'])] = item['quantity']
    session['cart'] = cart

    return redirect(url_for('checkout'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not mongo.db.users.find_one({'username': username}):
            hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            flash('Signup successful. You can now log in.', 'signup_success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.', 'signup_error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Password is incorrect.')
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        user = mongo.db.users.find_one({'username': username})
        if user:
            hashed_password = generate_password_hash(new_password)
            mongo.db.users.update_one({'username': username}, {'$set': {'password': hashed_password}})

            mongo.db.password_changes.insert_one({
                'username': username,
                'new_password': hashed_password,
                'timestamp': datetime.utcnow()
            })

            flash('Password changed.')
            return redirect(url_for('login'))
        else:
            flash('Username not found.')

    return render_template('forgot_password.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flashes = session.get('_flashes')
    if flashes:
        session['_flashes'] = [msg for msg in flashes if msg[1] in ['signup_success', 'success'] or msg[1] == '']
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
