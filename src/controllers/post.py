from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint('post', __name__, url_prefix='/posts')


def _create_post():
    data =  request.json
    post = User(title=data['title'],
                body=data['body'],
                author_id=data['author_id'])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            'id': user.id,
            'title': user.title,
            'body': user.body,
            'author_id': user.author_id,
        } 
        for user in users
    ]
