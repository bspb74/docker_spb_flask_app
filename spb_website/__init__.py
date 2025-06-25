# from datetime import timedelta
#
# from flask import Flask
# from flask_smorest import Api
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# from flask_login import LoginManager
# from flasgger import Swagger
# from flask_jwt_extended import JWTManager
#
#
# db = SQLAlchemy()
# DB_NAME = 'spb_db'
# api = Api()
#
#
# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'rplytq7gETnC7KWN1D7guj6cbtaUED5FZS6w0Kbkkr4ZBvmflXAB4QpM30HCxB8fmbOKJfHVt7O_iZEOiRgvsw'
#     app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
#     app.config['JSON_AS_ASCII'] = False
#     app.config['API_TITLE'] = "Product API"
#     app.config['API_VERSION'] = "v1"
#     app.config['OPENAPI_VERSION'] = "3.0.3"
#     app.config['OPENAPI_URL_PREFIX'] = "/docs"
#     app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger"
#     app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.5/"
#     app.config["JWT_SECRET_KEY"] = \
#         "26Vm4FPbqSUQP6glnMw_KqIwdRxAT8Il7n1oHLN475lDqI-cbZiDgq3POTm2Oa0CndEAPYpxwJh9kaJlp3G_mQ"
#     app.config["PROPAGATE_EXCEPTIONS"] = True
#     app.config["API_SPEC_OPTIONS"] = {
#         "components": {
#             "securitySchemes": {
#                 "Bearer Auth": {
#                     "type": "apiKey",
#                     "in": "header",
#                     "name": "Authorization",
#                     "bearerFormat": "JWT",
#                 }
#             }
#         }
#     }
#     app.config['OPENAPI_REDOC_PATH'] = "/redoc"
#     app.config['OPENAPI_REDOC_UI_URL'] = "https://cdn.jsdeliver.net/npm/redoc@next/bundles/redoc.standalone/"
#     app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://bspb74:b$pB742980@bspb-srv:3306/{DB_NAME}'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)
#     api.init_app(app)
#     jwt = JWTManager(app)
#     Swagger(app)
#
#     from .views import views
#     from .auth import auth
#     from .ProductApi import api_product
#     from .auth_with_api_key import auth_blp
#
#     app.register_blueprint(views, url_prefix="/")
#     app.register_blueprint(auth, url_prefix="/")
#     api.register_blueprint(api_product)
#     api.register_blueprint(auth_blp)
#
#     from .models import User
#
#     conn = check_conn(app)
#     if conn:
#         print('Connected to DB: ' + DB_NAME)
#         create_database(app)
#     else:
#         print('Not Connected!')
#
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)
#
#     @login_manager.user_loader
#     def load_user(id):
#         return User.query.get(int(id))
#
#     return app
#
#
# def create_database(app):
#     with app.app_context():
#         db.create_all()
#         print('Created Database!')
#
#
# def check_conn(app):
#     with app.app_context():
#         try:
#             with db.engine.connect() as connection:
#                 connection.execute(text("SELECT 1;"))
#                 return True
#         except Exception as e:
#             print(f"Database connection failed: {e}")
#             return False