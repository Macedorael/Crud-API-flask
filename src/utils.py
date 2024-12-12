from functools import wraps
from http import HTTPStatus
from src.app import db, User
from flask_jwt_extended import get_jwt_identity

def requires_role(allowed_roles=None):

    if allowed_roles is None:
        allowed_roles = ['Admin']
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name not in allowed_roles:
                return {'message': 'user do not have acess'}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)
        
        return wrapped
    
    return decorator
