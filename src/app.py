import os
from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click
import sqlalchemy as sa
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_jwt_extended import JWTManager



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate() #usado para versonamento de banco
jwt = JWTManager()

class Role(db.Model): 
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30), unique=True, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")
    
    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r}, active={self.active!r})"

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped[list["Role"]] = relationship(back_populates="user")
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
    

@click.command('init-db')
def init_db_command():
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY = 'super-secret',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

 
    
    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app, db) #usado para versonamento de banco

    #register blueprints
    from src.controllers import auth, user, post, role
    
    

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    jwt.init_app(app)

    
    return app