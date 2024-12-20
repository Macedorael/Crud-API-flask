import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from src.controllers import auth, user, post, role
from flask_bcrypt import Bcrypt

migrate = Migrate() #usado para versonamento de banco
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(environment=os.environ['ENVIRONMENT']):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'src.config.{environment.title()}Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    
    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    jwt.init_app(app)

    
    return app