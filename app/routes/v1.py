from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

from models.user import User
from objects import USER_CLIENT

app = APIRouter()


@app.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    if USER_CLIENT.create_user(user):
        return {'msg': 'User has been successfully created'}
    else:
        raise HTTPException(HTTP_409_CONFLICT, detail='User already existed')
