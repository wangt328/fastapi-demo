from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from libs.jwt import authenticate_user, create_jwt_token
from models.jwt import JWTUser

router = APIRouter()


@router.post('/token', tags=['authenticate'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user = JWTUser(username=form_data.username, password=form_data.password)
    user = authenticate_user(jwt_user)

    if user is None:
        # Pay attention, if you return HTTPException, it will be a 200 status code
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return jwt_token
