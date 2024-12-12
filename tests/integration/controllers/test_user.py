from http import HTTPStatus
from src.app import User, Role,db
from sqlalchemy import func

def test_get_user_cuccess(client):
    #criando uma role
    role = Role(name='Admin')
    db.session.add(role)
    db.session.commit()

    #criando um usuário
    user = User(username='john', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    #login
    response = client.post('auth/login', json={'username': 'john', 'password': 'test'})
    access_token = response.json['access_token']
    

    #then
    response = client.get(f'/users/{user.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == HTTPStatus.OK
    

def test_get_user_not_found(client):
    
    #criando uma role
    role = Role(name='Admin')
    db.session.add(role)
    db.session.commit()

    #criando um usuário para o login
    user = User(username='john', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    user_id= 10

    #login  
    response = client.post('auth/login', json={'username': 'john', 'password': 'test'})
    access_token = response.json['access_token']
    

    #when
    response = client.get(f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    
    
def test_create_user(client,access_token):
    
    role_id = db.session.execute(db.select(Role.id).where(Role.name == 'Admin')).scalar()
    payload = {
        'username': 'jane',
        'password': 'test',
        'role_id': role_id
    }

    #when
    response = client.post('/users/', json=payload, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'User created'}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2


def test_list_users(client,access_token):
    
    
    user = db.session.execute(db.select(User).where(User.username == 'john')).scalar()
    

    #when
    response = client.get(f'/users/', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'message': [
        {
            'id': user.id,
            'username': user.username,
            'role': {
                'id': user.role.id,
                'name': user.role.name
            },
        }
    ]}