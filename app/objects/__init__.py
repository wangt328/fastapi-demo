from configs.alpha import MONGODB_COLLECTION
from libs.mongodb.client import MongoDatabase
from libs.user.client import MongoUserClient
from libs.user.jwt_service import JWTService

MONGODB = MongoDatabase()

USER_CLIENT = MongoUserClient(MONGODB[MONGODB_COLLECTION['user_collection']])

JWT_SERVICE = JWTService(USER_CLIENT)
