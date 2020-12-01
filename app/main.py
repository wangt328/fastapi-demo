import logging.config

from fastapi import FastAPI, Depends

from objects import JWT_SERVICE
from routes.common import router as common_router
from routes.v1 import app as v1_app_router

# setup loggers
logging.config.fileConfig('configs/logging.conf', disable_existing_loggers=False)

# get root logger. the __name__ resolve to 'main' since we are at the root of the project.
# This will get the root logger since no logger in the configuration has this
# name.
# logger = logging.getLogger(__name__)


# 'Main' app used to set the '/' endpoint
app = FastAPI(
    title='Xinhua Bookstore API - Demo',
    description='Provides API endpoints for querying bookstore data',
    version='1.0.0',
    docs_url=None, redoc_url=None
)

# Mounts the common used endpoints and v1 API on the main API
app.include_router(common_router)
app.include_router(v1_app_router, prefix='/v1', dependencies=[Depends(JWT_SERVICE.check_jwt_token)])

# in cmd, run: `uvicorn run:app --reload --port 3000 --log-configs 'configs/logging.conf'`
