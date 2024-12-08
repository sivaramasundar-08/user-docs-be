import base64
import os
import uuid

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import requests
from requests import Response as RawResponse
from starlette import status
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import env_config
from app.schema import CommonResponseSchema, ErrorResponseSchema
from app.utils import logger


class AuthMiddleware(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        methods = ['POST', 'PUT', 'PATCH']
        content_type = request.headers.get('content-type')
        json_body = ""
        if request.method in methods and 'application/json' in content_type:
            await self.set_body(request)
            json_body = await request.json()
        request_id = str(uuid.uuid4())
        request_id = request_id.replace("-", "")
        with logger.contextualize(request_id=request_id):
            function_name: str = "Auth Middleware"
            logger.info(f"Enter - {function_name}")
            logger.info(f"Request Started URL: {request.url.path}, Method: {request.method}, Body: {json_body}")
            access_token = request.headers.get("access_token", "")
            if "/health" == request.url.path:
                response = await call_next(request)
                return response

            if access_token:
                if validate_access_token(access_token):
                    # claims = jwt.decode(access_token, options={"verify_signature": False})
                    claims = decode_access_token(token=access_token)
                    email = claims.get("email")
                    user_name = claims.get("username")
                    if email is None or email == "":
                        return JSONResponse(status_code=401, content={"msg": "Unauthorized"})
                    request.state.email_id = email
                    request.state.request_id = request_id
                    request.state.user_name = user_name
                    response = await call_next(request)
                    response_body = [section async for section in response.body_iterator]
                    response.body_iterator = iterate_in_threadpool(iter(response_body))
                    logger.info(f"Response Started URL: {request.url.path}, Method: {request.method}, Body: "
                                f"{response_body[0].decode()}")
                    return response
                logger.info(f"Exit - {function_name}")
            return JSONResponse(
                status_code=401,
                content=CommonResponseSchema(
                    message="Unauthorized", status="Not Ok"
                ).dict(),
            )


def validate_access_token(token: str) -> bool:
    function_name = "Validate Access Token"
    logger.info(f"Enter - {function_name}")
    try:
        data: dict = decode_access_token(token)
        logger.info(f"Exit - {function_name}")
        return bool(data.get("email", ""))
    except (
            ValueError,
    ) as jwt_error:
        logger.error(
            f"Exit - {function_name} Exception Occurred {jwt_error}",
        )
        raise jwt_error
    except (
            ExpiredSignatureError,
            InvalidTokenError,
    ) as jwt_error:
        logger.error(f"Exit {function_name} Exception occurred: {str(jwt_error)}")
        raise jwt_error


def decode_access_token(token: str) -> dict:
    function_name = "Decode Access Token"
    logger.info(f"Enter - {function_name}", function_name=function_name)
    try:
        if token:
            decoded_token: dict = jwt.decode(
                token, env_config.secret_key, algorithms=[env_config.algorithm]
            )
            return decoded_token
        else:
            raise ValueError("Please provide a valid access token")
    except (
        ValueError,
    ) as jwt_error:
        logger.error(
            f"Exit - {function_name} Exception Occurred {jwt_error}",
            )
        raise jwt_error
