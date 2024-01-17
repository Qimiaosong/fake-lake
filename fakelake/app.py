import os, uvicorn

from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fakelake.api import (datasource, datalake, datalake_export, data_analysis, data_dev, data_modeling,
                          depend, user, role, workspace, env_manager, job_manager)

from fakelake.version import __version__
from fakelake.settings import global_settings
from fakelake.config import load_config
from fastapi.common.log import init_log
from fakelake.compute_engine.async_status import start_status_job


cur_dir = os.path.dirname(os.path.abspath(__file__))


def _custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Do U Like Grapefruit",
        version=__version__,
        description="Grapefruit OpenAPI Schema",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app():
    app = FastAPI()
    add_pagination(app)

    _settings = global_settings()
    load_config()
    init_log(_settings.log.file_size, _settings.log.file_count, _settings.log.level)

    app.add_middleware(
        DBSessionMiddleware,
        db_url=f"postgresql://{_settings.db.username}:{_settings.db.password}@{_settings.db.port}/{_settings.db.dbname}"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static", StaticFiles(directory=f"{cur_dir}/static"), name="static")
    app.mount("/assets", StaticFiles(directory=f"{cur_dir}/static/assets"), name="assets")

    app.include_router(datasource.router, prefix="/datasource",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(datalake_export.router, prefix="/dataLakeExport",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(datalake.router, prefix="/datalake",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(data_modeling.router, prefix="/dataModeling",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(data_dev.router, prefix="/dataDev",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(data_analysis.router, prefix="/dataAnalysis",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license)])
    app.include_router(job_manager.router, prefix="/jobManager",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(env_manager.router, prefix="/envManager",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])
    app.include_router(user.router, prefix="/user")
    app.include_router(workspace.router, prefix="/workspace",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license)])
    app.include_router(role.router, prefix="/role",
                       dependencies=[Depends(depend.verify_token), Depends(depend.verify_license), Depends(depend.verify_permission)])

    app.openapi = _custom_openapi
    return app


app = create_app()
start_status_job()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 10100,
            "message": exc.errors(),
            "data": None
        })
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        })
    )


@app.get("/", tags=["Default"])
async def index():
    return FileResponse(f"{cur_dir}/static/index.html")


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, debug=True)