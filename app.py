from fastapi import FastAPI

from routes.authenticate import router as authenticate_router
from starlette.status import HTTP_200_OK


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


@app.get('/healthcheck', status_code=HTTP_200_OK)
def health_check() -> str:
    return 'ok'
