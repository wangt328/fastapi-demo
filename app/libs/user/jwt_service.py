from datetime import datetime, timedelta
from typing import Optional, List, NoReturn

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from configs.alpha import JWT_CONFIG
from libs.user.client import UserClient
from models.user import User

OAUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl='/token')


class JWTService(object):
    def __init__(self, user_client: UserClient):
        self._user_client = user_client

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate username and password to give JWT token

        :param username: username
        :param password: password
        :return: None or a valid JWTUser
        """
        return self._user_client.validate_user(username, password)

    @staticmethod
    def create_jwt_token(user: User) -> dict:
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
        return {'access_token': jwt_token}

    def check_jwt_token(self, token: str = Depends(OAUTH_SCHEMA)) -> NoReturn:
        """
        Check if the JWT token is valid

        :param token: JWT token to be validated
        :return:
        """
        try:
            jwt_payload = jwt.decode(token, JWT_CONFIG['private_key'], algorithm=JWT_CONFIG['algorithm'])
            username = jwt_payload.get('sub')
            roles = jwt_payload.get('roles')

            if self._user_client.query(username) is not None:
                if not self.is_entitled(roles):
                    raise HTTPException(HTTP_403_FORBIDDEN)
            else:
                raise HTTPException(HTTP_401_UNAUTHORIZED)
        except InvalidTokenError:
            raise HTTPException(HTTP_401_UNAUTHORIZED)

    @staticmethod
    def is_entitled(roles: List[str]) -> bool:
        """
        Check if the user is entitled to access the resource based on roles

        :param roles: roles associated with the user
        :return: true if the user is entitled
        """
        return 'admin' in roles

