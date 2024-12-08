import json
import time
import requests
from fastapi import HTTPException
from starlette import status
from sqlalchemy.exc import (
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session

from app.models import DynamicModelGenerator
from app.schema import (
    StateSchema,
    FilterRequestSchema,
    UserDocumentRequest,
    UpdateDocumentTagsRequest,
    DeleteDocumentRequest,
)

from app.utils import logger, identify_document_type, DBUtils


class UserDocsDB:

    @staticmethod
    def fetch_user_document(request_body: FilterRequestSchema, session: Session, state: StateSchema):
        function_name: str = "Fetch User Document - Database"
        try:
            print("State print")
            print(state.email_id)
            print(state.user_name)
            print(state.request_id)
            logger.info(f"Enter {function_name}")
            user_document_model = DynamicModelGenerator.generate_user_document_model()

            query_filters = [user_document_model.is_active == 1]
            query = DBUtils.make_query(
                additional_filters=query_filters,
                pre_query=None,
                filters=request_body,
                session=session,
                query_model=user_document_model,
            )
            user_documents: list[user_document_model] = query[0].all()
            total_count = query[1]
            logger.info(f"Exit {function_name}")
            return user_documents, total_count
        except (
                ProgrammingError,
                OperationalError,
                NoSuchTableError,
                NoSuchColumnError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error

    @staticmethod
    def upload_document(request_body: UserDocumentRequest, session: Session, state: StateSchema):
        function_name: str = "Upload Document - Database"
        try:
            logger.info(f"Enter {function_name}")
            document_type = identify_document_type(request_body.text)
            if document_type == "invalid":
                raise ValueError("Invalid document provided")
            user_document_model = DynamicModelGenerator.generate_user_document_model()
            user_document = user_document_model()
            user_document.is_active = 1
            user_document.created_at = int(time.time())
            user_document.updated_at = int(time.time())
            user_document.user_email = state.email_id
            user_document.pages = request_body.pages
            user_document.text = request_body.text
            user_document.tags = json.dumps(request_body.tags)
            user_document.document_type = document_type
            session.add(user_document)
            session.commit()
            logger.info(f"Exit {function_name}")
        except (
                ProgrammingError,
                OperationalError,
                NoSuchTableError,
                NoSuchColumnError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error

    @staticmethod
    def update_document_tags(request_body: UpdateDocumentTagsRequest, session: Session, state: StateSchema):
        function_name: str = "Update Document Tags - Database"
        try:
            logger.info(f"Enter {function_name}")
            user_document_model = DynamicModelGenerator.generate_user_document_model()
            user_document_filter = [
                user_document_model.is_active == 1,
                user_document_model.id == request_body.document_id,
            ]
            user_document_detail = session.query(user_document_model).filter(*user_document_filter).first()
            if user_document_detail is None:
                raise ValueError("User Document not found")

            if user_document_detail.user_email != state.email_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authorized to update this document"
                )

            user_document_detail.updated_at = int(time.time())
            user_document_detail.tags = json.dumps(request_body.tags)
            session.commit()
            logger.info(f"Exit {function_name}")
        except (
                ProgrammingError,
                OperationalError,
                NoSuchTableError,
                NoSuchColumnError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error

    @staticmethod
    def delete_document(request_body: DeleteDocumentRequest, session: Session, state: StateSchema):
        function_name: str = "Delete Document - Database"
        try:
            logger.info(f"Enter {function_name}")
            user_document_model = DynamicModelGenerator.generate_user_document_model()
            user_document_filter = [
                user_document_model.is_active == 1,
                user_document_model.id == request_body.document_id,
            ]
            user_document_detail = session.query(user_document_model).filter(*user_document_filter).first()
            if user_document_detail is None:
                raise ValueError("User Document not found")

            if user_document_detail.user_email != state.email_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authorized to delete this document"
                )

            user_document_detail.is_active = 0
            user_document_detail.updated_at = int(time.time())
            session.commit()
            logger.info(f"Exit {function_name}")
        except (
                ProgrammingError,
                OperationalError,
                NoSuchTableError,
                NoSuchColumnError,
        ) as internal_error:
            logger.error(f"Exit - {function_name} Exception occurred: {internal_error}")
            raise internal_error
