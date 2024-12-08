from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.exc import (
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.connection import get_session
from app.service import UserDocsService
from app.utils import logger, state_parser
from app.schema import (
    StateSchema,
    ErrorResponseSchema,
    DataResponseSchema,
    FilterRequestSchema,
    UserDocumentRequest,
    UpdateDocumentTagsRequest,
    DeleteDocumentRequest
)

user_router = APIRouter(prefix="/docs", tags=["User Docs"])


@user_router.post("/fetch-all")
def fetch_user_document(request: Request, request_body: FilterRequestSchema, session: Session = Depends(get_session)):
    function_name: str = "Fetch User Document - Controller"
    try:
        logger.info(f"Enter {function_name}")
        state: StateSchema = state_parser(request.state)
        response = UserDocsService.fetch_user_document(
            session=session, state=state, request_body=request_body
        )
        headers = {"traceid": state.request_id}
        logger.info(f"Exit {function_name}")
        return JSONResponse(
            content=response.dict(by_alias=True),
            status_code=status.HTTP_200_OK,
            headers=headers
        )
    except (
            OperationalError,
            ProgrammingError,
            NoSuchColumnError,
            NoSuchTableError,
    ) as operational_error:
        logger.error(f"Exit - {function_name} Exception occurred: {operational_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail="Database error",
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as value_error:
        logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@user_router.post("/upload")
def upload_document(request: Request, request_body: UserDocumentRequest, session: Session = Depends(get_session)):
    function_name: str = "Upload Document - Controller"
    try:
        logger.info(f"Enter {function_name}")
        state: StateSchema = state_parser(request.state)
        response: DataResponseSchema = UserDocsService.upload_document(
            session=session, state=state, request_body=request_body
        )
        headers = {"traceid": state.request_id}
        logger.info(f"Exit {function_name}")
        return JSONResponse(
            content=response.dict(by_alias=True),
            status_code=status.HTTP_200_OK,
            headers=headers
        )
    except (
            OperationalError,
            ProgrammingError,
            NoSuchColumnError,
            NoSuchTableError,
    ) as operational_error:
        logger.error(f"Exit - {function_name} Exception occurred: {operational_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail="Database error",
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as value_error:
        logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@user_router.post("/update-tags")
def update_document_tags(request: Request, request_body: UpdateDocumentTagsRequest, session: Session = Depends(get_session)):
    function_name: str = "Update Document Tags - Controller"
    try:
        logger.info(f"Enter {function_name}")
        state: StateSchema = state_parser(request.state)
        response: DataResponseSchema = UserDocsService.update_document_tags(
            session=session, state=state, request_body=request_body
        )
        headers = {"traceid": state.request_id}
        logger.info(f"Exit {function_name}")
        return JSONResponse(
            content=response.dict(by_alias=True),
            status_code=status.HTTP_200_OK,
            headers=headers
        )
    except (
            OperationalError,
            ProgrammingError,
            NoSuchColumnError,
            NoSuchTableError,
    ) as operational_error:
        logger.error(f"Exit - {function_name} Exception occurred: {operational_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail="Database error",
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as value_error:
        logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except HTTPException as http_exception:
        logger.error(f"Exit - {function_name} Exception occurred: {http_exception}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(http_exception),
            ).dict(),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@user_router.post("/delete")
def delete_document(request: Request, request_body: DeleteDocumentRequest, session: Session = Depends(get_session)):
    function_name: str = "Delete Document - Controller"
    try:
        logger.info(f"Enter {function_name}")
        state: StateSchema = state_parser(request.state)
        response: DataResponseSchema = UserDocsService.delete_document(
            session=session, state=state, request_body=request_body
        )
        headers = {"traceid": state.request_id}
        logger.info(f"Exit {function_name}")
        return JSONResponse(
            content=response.dict(by_alias=True),
            status_code=status.HTTP_200_OK,
            headers=headers
        )
    except (
            OperationalError,
            ProgrammingError,
            NoSuchColumnError,
            NoSuchTableError,
    ) as operational_error:
        logger.error(f"Exit - {function_name} Exception occurred: {operational_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail="Database error",
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as value_error:
        logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except HTTPException as http_exception:
        logger.error(f"Exit - {function_name} Exception occurred: {http_exception}")
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Unsuccessful - Exception occurred",
                status="Not Ok",
                error_detail=str(http_exception),
            ).dict(),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


