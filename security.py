from werkzeug.security import safe_str_cmp
from App.models import User
from App import jwt

@jwt.authentication_handler
def authenticate(email, password):   
    user = User.query.filter_by(email=email).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
@jwt.identity_handler 
def identity(payload):
    id = payload['identity']
    return User.query.filter_by(id=id).first()  