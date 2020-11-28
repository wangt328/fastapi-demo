from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from libs.jwt import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser

router = APIRouter()


@router.post('/token', tags=['authenticate'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {
        'username': form_data.username,
        'password': form_data.password
    }

    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)

    if user is None:
        # Pay attention, if you return HTTPException, it will be a 200 status code
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return jwt_token
