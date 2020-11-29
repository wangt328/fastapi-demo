from fastapi import File, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from bookstoreapp.libs.jwt import authenticate_user, create_jwt_token
from bookstoreapp.models import User, Book
from bookstoreapp.models.jwt import JWTUser

app = APIRouter(openapi_prefix='/v1')
oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')


@app.post('/user', status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {'request_body': user}


@app.get('/user')
async def get_user_validation(password: str):
    return password


@app.get('/book/{isbn}', response_model=Book, response_model_exclude=['year'])
async def get_book_by_isbn(isbn: str):
    book = {'isbn': '1', 'name': '2', 'year': 4}
    return Book(**book)


@app.post("/user/photo")
async def upsert_photo(profile_photo: bytes = File(...)):
    return len(profile_photo)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {
        'username': form_data.username,
        'password': form_data.password
    }

    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)

    if user is None:
        return HTTP_401_UNAUTHORIZED

    jwt_token = create_jwt_token(user)
    return jwt_token

