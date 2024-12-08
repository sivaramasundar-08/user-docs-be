import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config.constants import Constants
from app.database import UserDocsDB
from app.schema import (
    StateSchema,
    CommonResponseSchema,
    ErrorResponseSchema,
    DataResponseSchema,
    FilterRequestSchema,
    UserDocumentRequest,
    UpdateDocumentTagsRequest,
    DeleteDocumentRequest,
    UserDocumentsResponse,
    UserDocumentsResponseWithTotalCount
)
from sqlalchemy.exc import (
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)

from app.utils import logger


class UserDocsService:
    @staticmethod
    def fetch_user_document(session: Session, request_body: FilterRequestSchema, state: StateSchema) -> DataResponseSchema:
        function_name: str = "Fetch User Document - Service"
        try:
            logger.info(f"Enter {function_name}")
            db_response, total_count = UserDocsDB.fetch_user_document(
                session=session,
                state=state,
                request_body=request_body
            )

            data_response = []
            for data in db_response:
                user_document = UserDocumentsResponse()
                if not data.tags:
                    user_document.tags = []
                else:
                    user_document.tags = json.loads(data.tags)
                user_document.id = data.id
                user_document.created_at = data.created_at
                user_document.updated_at = data.updated_at
                user_document.user_email = data.user_email
                user_document.pages = data.pages
                user_document.text = data.text
                user_document.document_type = data.document_type
                data_response.append(user_document)

            user_document_response = UserDocumentsResponseWithTotalCount()
            user_document_response.user_documents = data_response
            user_document_response.total = total_count
            response = DataResponseSchema(
                status="Ok",
                message="User documents fetched successfully",
                data=user_document_response,
            )
            logger.info(f"Exit {function_name}")
            return response
        except (
                ProgrammingError,
                OperationalError,
                NoSuchColumnError,
                NoSuchTableError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error
        except ValueError as value_error:
            logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
            raise value_error

    @staticmethod
    def upload_document(session: Session, request_body: UserDocumentRequest, state: StateSchema) -> DataResponseSchema:
        function_name: str = "Upload Document - Service"
        try:
            logger.info(f"Enter {function_name}")
            if not request_body.pages or not request_body.text or not request_body.tags:
                raise ValueError("Field required")
            UserDocsDB.upload_document(
                session=session,
                state=state,
                request_body=request_body
            )
            response: CommonResponseSchema = CommonResponseSchema(
                status="Ok",
                message="User document uploaded successfully",
            )
            logger.info(f"Exit {function_name}")
            return response
        except (
                ProgrammingError,
                OperationalError,
                NoSuchColumnError,
                NoSuchTableError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error
        except ValueError as value_error:
            logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
            raise value_error

    @staticmethod
    def update_document_tags(request_body: UpdateDocumentTagsRequest, session: Session, state: StateSchema):
        function_name: str = "Update Document Tags - Service"
        try:
            logger.info(f"Enter {function_name}")
            if not request_body.document_id or not request_body.tags:
                raise ValueError("Document ID and tags are required")

            UserDocsDB.update_document_tags(
                session=session,
                state=state,
                request_body=request_body
            )
            response: CommonResponseSchema = CommonResponseSchema(
                status="Ok",
                message="Document tags updated successfully",
            )
            logger.info(f"Exit {function_name}")
            return response
        except (
                ProgrammingError,
                OperationalError,
                NoSuchColumnError,
                NoSuchTableError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error
        except ValueError as value_error:
            logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
            raise value_error
        except HTTPException as http_exception:
            logger.error(f"Exit - {function_name} Exception occurred: {http_exception}")
            raise http_exception

    @staticmethod
    def delete_document(request_body: DeleteDocumentRequest, session: Session, state: StateSchema):
        function_name: str = "Delete Document - Service"
        try:
            logger.info(f"Enter {function_name}")
            if not request_body.document_id:
                raise ValueError("Document ID field required")

            UserDocsDB.delete_document(
                session=session,
                state=state,
                request_body=request_body
            )
            response: CommonResponseSchema = CommonResponseSchema(
                status="Ok",
                message="Document deleted successfully",
            )
            logger.info(f"Exit {function_name}")
            return response
        except (
                ProgrammingError,
                OperationalError,
                NoSuchColumnError,
                NoSuchTableError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error
        except ValueError as value_error:
            logger.error(f"Exit - {function_name} Exception occurred: {value_error}")
            raise value_error
        except HTTPException as http_exception:
            logger.error(f"Exit - {function_name} Exception occurred: {http_exception}")
            raise http_exception
