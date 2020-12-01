import logging
from typing import Optional, List

import pymongo
from passlib.context import CryptContext

from models.user import User

PWD_CONTEXT = CryptContext(schemes=['bcrypt'])

logger = logging.getLogger(__name__)


class UserClient:
    """Base class of user database client"""
    def query(self, username: str) -> Optional[User]:
        raise NotImplementedError

    def create_user(self, user: User) -> bool:
        raise NotImplementedError

    def delete_user(self, username: str) -> bool:
        raise NotImplementedError

    def validate_user(self, username: str, password: str) -> Optional[User]:
        user = self.query(username)
        if (user is None) or (not user.active) or (not self.verify_password(password, user.password)):
            return None
        else:
            return user

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return PWD_CONTEXT.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)


class MongoUserClient(UserClient):
    def __init__(self, collection: pymongo.collection):
        self._collection = collection

    def list_users(self) -> List[User]:
        cursor = self._collection.find()

        return [User(**user) for user in cursor]

    def query(self, username: str) -> Optional[User]:
        query = {'username': {'$eq': username}}
        cursor = self._collection.find(query, {'_id': False})
        result = list(cursor)

        if len(result):
            return User(**result[0])
        else:
            return None

    def create_user(self, user: User) -> bool:
        if self.query(user.username) is not None:
            logger.info(f'Failed to create new user with username {user.username}, user already existed')
            return False

        user.password = self.get_hashed_password(user.password)
        user.active = True
        user.roles.append('visitor')

        self._collection.update_one({'username': user.username}, {'$set': user.dict()}, upsert=True)
        logger.info(f'Successfully create new user with username {user.username}')
        return True

    def delete_user(self, username: str) -> bool:
        self._collection.update_one({'username': username}, {'$set': {'active': False}}, upsert=False)
        return True

    @property
    def collection(self):
        return self._collection

