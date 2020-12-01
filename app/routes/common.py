from fastapi import Depends, APIRouter, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from objects import JWT_SERVICE

router = APIRouter()


# /token endpoint
@router.post('/token', tags=['Default'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = JWT_SERVICE.authenticate_user(form_data.username, form_data.password)

    if user is None or user.active is False:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = JWT_SERVICE.create_jwt_token(user)
    return jwt_token


# /login endpoint
@router.post('/login', tags=['User'])
async def post_user_validation(username: str = Body(...), password: str = Body(...)):
    if JWT_SERVICE.authenticate_user(username, password) is None:
        return {'is_valid': False}
    else:
        return {'is_valid': True}


# /heathcheck endpoint
@router.get('/healthcheck', status_code=HTTP_200_OK, tags=['Default'])
async def health_check() -> str:
    return 'ok'
