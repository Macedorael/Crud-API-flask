from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint('post', __name__, url_prefix='/posts')


def _create_post():
    data =  request.json
    post = Post(title=data['title'],
                body=data['body'],
                author_id=data['author_id'])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'author_id': post.author_id,
        } 
        for post in posts
    ]

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        _create_post()
        return {'message': 'Post created'}, HTTPStatus.CREATED
    else:
        return {'message': _list_posts()}
    
@app.route('/<int:post_id>')
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'author_id': post.author_id
    }