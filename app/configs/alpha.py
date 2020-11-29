JWT_CONFIG = {
    'private_key': '',  # cmd: openssl rand -hex 32
    'algorithm': 'HS256',
    'expiration': 60
}

MONGODB_CONFIG = {
    'host': '',
    'port': 27017,
    'username': '',
    'password': '',
    'db': ''
}

MONGODB_COLLECTION = {
    'user_collection': 'users',
}

