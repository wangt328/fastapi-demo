from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK
)

from models.user import User
from objects import USER_CLIENT, JWT_SERVICE

app = APIRouter()


@app.post('/user', status_code=HTTP_201_CREATED, tags=['User'])
async def post_user(user: User, roles: List[str] = Depends(JWT_SERVICE.check_jwt_token)):
    if 'admin' not in roles:
        raise HTTPException(HTTP_403_FORBIDDEN, detail='Only admin can create new user')

    if USER_CLIENT.create_user(user):
        return {'msg': 'User has been successfully created'}
    else:
        raise HTTPException(HTTP_409_CONFLICT, detail='User already existed')


@app.delete('/user/{username}', status_code=HTTP_200_OK, tags=['User'])
async def delete_user(username: str, roles: List[str] = Depends(JWT_SERVICE.check_jwt_token)):
    if 'admin' not in roles:
        raise HTTPException(HTTP_403_FORBIDDEN, detail='Only admin can delete new user')

    USER_CLIENT.delete_user(username)
    return {'msg': 'User has been successfully deleted'}


@app.get('/user/list', status_code=HTTP_200_OK, tags=['User'])
async def get_user_list(roles: List[str] = Depends(JWT_SERVICE.check_jwt_token)) -> List[User]:
    if 'admin' not in roles:
        raise HTTPException(HTTP_403_FORBIDDEN, detail='Only admin can list users')

    return USER_CLIENT.list_users()
