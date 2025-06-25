from sqlalchemy.orm import validates
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    pwd = db.Column(db.String(150))
    fName = db.Column(db.String(150))
    lName = db.Column(db.String(150))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30))
    prodName = db.Column(db.String(150))
    prodType = db.Column(db.String(150))
    imgName = db.Column(db.String(150))
    price = db.Column(db.Numeric(precision=10, scale=2))
    prodDesc = db.Column(db.String(10000))
    stockQty = db.Column(db.Integer)


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    cart_items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan', lazy='selectin')

    @property
    def cart_amount(self):
        return sum(item.product.product_price * item.quantity for item in self.cart_items)

    @property
    def cart_quantity(self):
        return sum(item.quantity for item in self.cart_items)

    def to_dict(self):
        return {
            'id': self.id,
            'products': [
                {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'product_price': item.product.product_price,
                    'total_price': item.product.product_price * item.quantity,
                    'product_name': item.product.product_name,
                    'product_image': f"/images/{item.product.product_image}",
                    'product_description': item.product.product_description,
                    'product_quantity': item.product.product_quantity,
                }
                for item in self.cart_items
            ]
        }

    def __repr__(self):
        return f"<Cart id={self.id}>"


class CartItem(db.Model):
    __tablename__ = 'cartitem'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Cart', back_populates='cart_items')

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return quantity

    def to_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'product': self.product.to_dict()
        }





