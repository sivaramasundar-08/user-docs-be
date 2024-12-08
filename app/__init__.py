from dotenv import load_dotenv
from fastapi import FastAPI
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse

from app.connection import create_table_user_documents
from app.controller import public_app
from app.config.constants import Constants
from app.schema import CommonResponseSchema
from app.utils.logger import logger

load_dotenv()


def create_fast_app() -> FastAPI:
    base_app = FastAPI(
            middleware=[
                    Middleware(GZipMiddleware, minimum_size=1000),
                    Middleware(
                            CORSMiddleware,
                            allow_origins=["*"],
                            allow_credentials=True,
                            allow_methods=["*"],
                            allow_headers=["*"],
                            ),
                    ],
            )
    return base_app


app: FastAPI = create_fast_app()


@app.get("/ping", tags=["Health Check"])
def ping():
    function_name = "Ping - Health Check"
    logger.info(
            message=f"Enter - {function_name}",
            function_name=function_name,
            )
    return JSONResponse(
            CommonResponseSchema(
                    message="Health check ping working for public", status="Ok"
                    ).dict(),
            status_code=status.HTTP_200_OK,
            )


@app.on_event("startup")
def create_table():
    create_table_user_documents()


app.mount(
    Constants.public_base_route,
    public_app,
)

