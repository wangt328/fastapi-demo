from typing import Set, Optional

from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')

PWD_CONTEXT = CryptContext(schemes=['bcrypt'])
jwt_user1 = {
    'username': 'test',
    'password': 'pss1',
    'active': True,
    'role': set('admin')
}

fake_jwt_user1 = JWTUser(**jwt_user1)


def get_hashed_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


# Authenticate username and password to give JWT token
def authenticate_user(user: JWTUser) -> Optional[JWTUser]:
    if fake_jwt_user1.username == user.username and \
            verify_password(user.password, fake_jwt_user1.password):
        # should read active status and roles from the database
        user.active = True
        user.roles.add('admin')
        return user
    else:
        return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    jwt_payload = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'roles': user.roles
    }
    jwt_token = jwt.encode(jwt_payload, 'secret_key', algorithm='HS256')
    return {'token': jwt_token}


# Check JWT token is correct or not
def check_jwt_token(token: str = Depends(oauth_schema)):
    jwt_payload = jwt.decode(token, 'secret_key', algorithm='HS256')
    username = jwt_payload.get('sub')
    expiration = jwt_payload.get('exp')
    roles = jwt_payload.get('roles')

    if datetime.utcnow() < expiration and fake_jwt_user1.username == username:
        return final_checks(roles)
    else:
        return False


def final_checks(roles: Set[str]) -> bool:
    return 'admin' in roles
