from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
import marshmallow as ma

from models import User


class UserSchema(ma.Schema):
    email = ma.fields.String()
    pwd = ma.fields.String()
    fName = ma.fields.String()
    lName = ma.fields.String()


auth_blp = Blueprint("api_auth", __name__, url_prefix='/api/v1/auth', description="Authentication operations")


@auth_blp.route("/login")
class UserLogin(MethodView):
    @auth_blp.arguments(UserSchema)
    def post(self, login_data):
        print("checking for user: %s" % login_data['email'])
        user = User.query.filter_by(email=login_data['email']).first()
        if user.email == login_data["email"] and check_password_hash(user.pwd, login_data["pwd"]):
            access_token = create_access_token(identity=user.email)
            return {"access_token": access_token}, 200
        abort(401, message="Invalid credentials")