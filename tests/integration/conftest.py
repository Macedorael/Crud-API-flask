import pytest
from src.app import create_app, db, User, Role

@pytest.fixture
def app():
    app = create_app(environment='testing')
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

@pytest.fixture
def access_user(client):
    #criando uma role
    role = Role(name='Admin')
    db.session.add(role)
    db.session.commit()

    #criando um usuário para o login
    user = User(username='john', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    reposponse = client.post('/users/', json={'username': 'john', 'password': 'test', 'role_id': role.id})
    return reposponse

