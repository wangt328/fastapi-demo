from typing import Callable

from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import Response

from libs.jwt import check_jwt_token
from routes.authenticate import router as authenticate_router
from starlette.status import HTTP_200_OK
from starlette.requests import Request

# "Main" app used to set the '/' endpoint
app = FastAPI(
    title='Xinhua Bookstore API - Demo',
    description='Provides API endpoints for querying bookstore data'
)

# v1_app used to set the endpoints with the '/v1' prefix
v1_app = FastAPI(
    title='version 1.0 API',
    description='API endpoints version 1.0, which will be rendered under /v1'
)

v1_app.include_router(authenticate_router)

# Mounts the v1 API on the main API to include the standard prefix
app.mount('/v1', v1_app)


# /heathcheck end point
@app.get('/healthcheck', status_code=HTTP_200_OK)
def health_check() -> str:
    return 'ok'


# middleware to check access token
@app.middleware('http')
async def middleware(request: Request, call_next: Callable):
    if not str(request.url).__contains__('/token'):
        jwt_token = request.headers['Authorization'].split('Bearer ')[1]
        try:
            check_jwt_token(jwt_token)
        except HTTPException as e:
            return Response(e.detail, e.status_code)

    response = await call_next(request)
    return response

# to run within the Pycharm, in cmd, run: `uvicorn main:app --reload --port 3000`
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
