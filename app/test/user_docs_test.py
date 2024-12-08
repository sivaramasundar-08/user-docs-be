import uuid
import pytest
from unittest.mock import MagicMock
from unittest import mock

from app.schema import (
    StateSchema,
    CommonResponseSchema,
    DataResponseSchema,
    ErrorResponseSchema,
    UserDocumentsResponseWithTotalCount
)
from app.service import UserDocsService
from app.database import UserDocsDB
from app.test import fetch_user_docs_mock
from app.test.request import RequestBody



@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db
    db.close()


state = StateSchema()
state.email_id = "test@gmail.com"
state.user_name = "Test User"
state.request_id = str(uuid.uuid4())


def test_fetch_user_docs(mock_db, mocker):
    request_body = RequestBody.filter_request
    mock_fetch = mocker.patch.object(UserDocsDB, 'fetch_user_document', return_value=(fetch_user_docs_mock().user_documents, 1))
    response = UserDocsService.fetch_user_document(mock_db, request_body, state)

    assert isinstance(response, DataResponseSchema)
    assert response.status == "Ok"
    assert response.message == "User documents fetched successfully"

    assert isinstance(response.data, UserDocumentsResponseWithTotalCount)
    assert len(response.data.user_documents) == 1
    assert response.data.total == 1

    mock_fetch.assert_called_once_with(
        session=mock_db,
        state=state,
        request_body=request_body
    )


def test_upload_docs_success(mock_db, mocker):
    request_body = RequestBody.upload_document_request
    mock_upload = mocker.patch.object(UserDocsDB, 'upload_document', return_value=None)
    response = UserDocsService.upload_document(mock_db, request_body, state)

    assert isinstance(response, CommonResponseSchema)
    assert response.status == "Ok"
    assert response.message == "User document uploaded successfully"

    mock_upload.assert_called_once_with(
        session=mock_db,
        state=state,
        request_body=request_body
    )


def test_upload_docs_failure_missing_required_fields(mock_db, mocker):
    request_body = RequestBody.upload_document_request.copy()
    request_body.tags = []
    request_body.pages = 0
    request_body.text = ""

    mock_upload = mocker.patch.object(UserDocsDB, 'upload_document')
    try:
        UserDocsService.upload_document(mock_db, request_body, state)
    except ValueError as value_error:
        assert str(value_error) == "Field required"

    mock_upload.assert_not_called()


def test_update_document_tags_success(mock_db, mocker):
    request_body = RequestBody.update_document_tags_request
    mock_update = mocker.patch.object(UserDocsDB, 'update_document_tags', return_value=None)
    response = UserDocsService.update_document_tags(request_body, mock_db, state)

    assert isinstance(response, CommonResponseSchema)
    assert response.status == "Ok"
    assert response.message == "Document tags updated successfully"

    mock_update.assert_called_once_with(
        session=mock_db,
        state=state,
        request_body=request_body
    )


def test_update_document_tags_failure_missing_required_fields(mock_db, mocker):
    request_body = RequestBody.update_document_tags_request.copy()
    request_body.document_id = 0
    request_body.tags = []

    mock_upload = mocker.patch.object(UserDocsDB, 'update_document_tags')
    try:
        UserDocsService.update_document_tags(request_body, mock_db, state)
    except ValueError as value_error:
        assert str(value_error) == "Document ID and tags are required"

    mock_upload.assert_not_called()


def test_delete_docs_success(mock_db, mocker):
    request_body = RequestBody.update_document_tags_request
    mock_update = mocker.patch.object(UserDocsDB, 'delete_document', return_value=None)
    response = UserDocsService.delete_document(request_body, mock_db, state)

    assert isinstance(response, CommonResponseSchema)
    assert response.status == "Ok"
    assert response.message == "Document deleted successfully"

    mock_update.assert_called_once_with(
        session=mock_db,
        state=state,
        request_body=request_body
    )


def test_delete_docs_failure_missing_required_fields(mock_db, mocker):
    request_body = RequestBody.delete_document_request.copy()
    request_body.document_id = 0

    mock_upload = mocker.patch.object(UserDocsDB, 'delete_document')
    try:
        UserDocsService.delete_document(request_body, mock_db, state)
    except ValueError as value_error:
        assert str(value_error) == "Document ID field required"

    mock_upload.assert_not_called()

