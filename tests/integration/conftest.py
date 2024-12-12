import pytest
from src.app import create_app, db, User, Role

@pytest.fixture
def app():
    app = create_app({
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET_KEY": 'test',
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all
        

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(client):
    #criando uma role
    role = Role(name='Admin')
    db.session.add(role)
    db.session.commit()

    #criando um usuário para o login
    user = User(username='john', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    #login
    response = client.post('auth/login', json={'username': 'john', 'password': 'test'})
    return response.json['access_token']


