from http import HTTPStatus
from src.app import Post,db,User,Role
from sqlalchemy import func

def test_list_post(client,access_user):
    
    user = db.session.execute(db.select(User).where(User.username == 'john')).scalar()
    post = Post(title='vamos nessa', body='vamos nessa? vamos mesmo!', author_id=user.id, )
    db.session.add(post)
    db.session.commit()

    #when
    response = client.get('/posts/')

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'message': [{'id': post.id, 'title': post.title, 'body': post.body, 'author_id': post.author_id}]}

def test_create_post(client,access_user):
    user = db.session.execute(db.select(User).where(User.username == 'john')).scalar()

    payload = {
        'title': 'vamos nessa',
        'body': 'vamos nessa? aagora!',
        'author_id': user.id
    }

    #when
    response = client.post('/posts/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'Post created'}
    assert db.session.execute(db.select(func.count(Post.id))).scalar() == 1
    



