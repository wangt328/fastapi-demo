import time
from datetime import datetime, timedelta
from typing import Optional, List, NoReturn

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from bookstoreapp.config.alpha import JWT_CONFIG
from bookstoreapp.models.jwt import JWTUser, JWToken

OAUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl='/token')

PWD_CONTEXT = CryptContext(schemes=['bcrypt'])

fake_jwt_user_dict = {
    'username': 'test',
    'password': '$2b$12$W37ZSNTB.l21Y2KVcWkGe.HXVBb45bF1SHsNj4dEDqav8N6nbPlKm',
    'active': True,
    'role': set('admin')
}

fake_jwt_user = JWTUser(**fake_jwt_user_dict)


def get_hashed_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def authenticate_user(user: JWTUser) -> Optional[JWTUser]:
    """
    Authenticate username and password to give JWT token

    :param user: a JWTUser to be authenticated
    :return: None or a valid JWTUser
    """
    if fake_jwt_user.username == user.username and \
            verify_password(user.password, fake_jwt_user.password):
        # should read active status and roles from the database
        user.active = True
        user.roles.append('admin')
        return user
    else:
        return None


def create_jwt_token(user: JWTUser) -> JWToken:
    """
    Create JWT token for a valid user

    :param user: JWTUser
    :return: a dictionary that contains the token string
    """
    jwt_payload = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_CONFIG['expiration']),
        'roles': user.roles
    }
    jwt_token = jwt.encode(jwt_payload, JWT_CONFIG['private_key'], algorithm=JWT_CONFIG['algorithm'])
    return JWToken(token=jwt_token)


def check_jwt_token(token: str = Depends(OAUTH_SCHEMA)) -> NoReturn:
    """
    Check if the JWT token is valid

    :param token: JWT token to be validated
    :return:
    """
    try:
        jwt_payload = jwt.decode(token, JWT_CONFIG['private_key'], algorithm=JWT_CONFIG['algorithm'])
        username = jwt_payload.get('sub')
        roles = jwt_payload.get('roles')

        if fake_jwt_user.username == username:
            if not is_entitled(roles):
                raise HTTPException(HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(HTTP_401_UNAUTHORIZED)
    except InvalidTokenError:
        raise HTTPException(HTTP_401_UNAUTHORIZED)


def is_entitled(roles: List[str]) -> bool:
    """
    Check if the user is entitled to access the resource based on roles

    :param roles: roles associated with the user
    :return: true if the user is entitled
    """
    return 'admin' in roles

