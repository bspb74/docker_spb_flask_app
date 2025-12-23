from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from models import Product, CartItem

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/user_settings')
@login_required
def user_settings():
    return render_template("user_settings.html", user=current_user)


@views.route('/cart')
@login_required
def cart():
    return render_template("cart.html", user=current_user)


@views.route('/contact')
def contact():
    return render_template("contact.html")


@views.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    if request.method != "POST":
        try:
            selected = request.args.get("selected")
            print("Selected from URL: %s" % selected)
        except Exception as e:
            print(e)
    else:
        selected = request.form.get("filter_items")
        print("Selected from Form: %s" % selected)
        return redirect(url_for("views.products", selected=selected))

    page = request.args.get('page', 1, type=int)
    if selected is not None and selected != "all":
        products = Product.query.filter_by(prodType=selected).paginate(page=page, per_page=3)
        print("Pages: %s" % products.items)
    else:
        # products = db.session.execute(db.select(Product)).paginate(page=page, per_page=6, error_out=False)
        products = Product.query.all()

    next_url = None
    try:
        next_url = url_for('views.products', page=products.next_num, selected=selected) \
            if products.has_next else None
        print("Next URL: %s" % next_url)
    except Exception as e:
        print(e)
    prev_url = None
    try:
        prev_url = url_for('views.products', page=products.prev_num, selected=selected) \
            if products.has_prev else None
        print("Previous URL: %s" % prev_url)
    except Exception as e:
        print(e)

    return render_template("products.html", user=current_user, product=products,
                       selected=selected,
                       next_url=next_url,
                       prev_url=prev_url)


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add_item_to_cart():

    if request.method == "GET":
        prod_id = request.args.get('product_id')
        print("Prod ID: %s" % prod_id)
        product = Product.query.filter_by(id=prod_id).first()
        print("Product: %s" % product.prodName)

        if 'user_id' in session:
            print("User ID: %s" % session['user_id'])

        if 'cart' not in session:
            session['cart'] = {}
        cart = session['cart']

    return redirect(url_for('views.products'))


@views.route('/editcart/<int:product_id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def get_patch_delete_by_id(product_id):
    cartItem = CartItem.query.filter_by(product_id=product_id).first()

    if not cartItem:
        return jsonify({'error': 'Cart Item does not exist'}), 404

    if request.method == 'GET':
        return jsonify(cartItem.to_dict()), 200

    if request.method == 'PATCH':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'There is no data to update'}), 404

        allowed_fields = ['quantity']

        for key, value in data.items():
            if key in allowed_fields:
                setattr(cartItem, key, value)

        # try:
        #     db.session.commit()
        #     return jsonify(cartItem.to_dict()), 200
        # except Exception as e:
        #     db.session.rollback()
        #     return jsonify({'error': f'Failed to update cart Item: {str(e)}'}), 500

    if request.method == 'DELETE':
        pass
        # try:
        #     db.session.delete(cartItem)
        #     db.session.commit()
        #     return jsonify({'message': 'Cart Item deleted successfully'}), 200
        # except Exception as e:
        #     db.session.rollback()
        #     return jsonify({'error': f'Failed to delete Cart item: {str(e)}'}), 500