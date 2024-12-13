import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from src.controllers import auth, user, post, role

migrate = Migrate() #usado para versonamento de banco
jwt = JWTManager()


def create_app(environment=os.environ['ENVIRONMENT']):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'src.config.{environment.title()}Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    migrate.init_app(app, db) #usado para versonamento de banco

    #register blueprints
    
    
    

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    jwt.init_app(app)

    
    return app