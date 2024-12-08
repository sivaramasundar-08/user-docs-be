import json

import time
from app.schema import UserDocumentsResponse, UserDocumentsResponseWithTotalCount


def fetch_user_docs_mock():
    data_response = []
    user_document = UserDocumentsResponse()
    user_document.id = 1
    user_document.user_email = "test@gmail.com"
    user_document.created_at = int(time.time())
    user_document.updated_at = int(time.time())
    user_document.document_type = "ID Card"
    user_document.pages = 10,
    user_document.text = "This is a sample ID card document. ID Number: 987654321, Date of Birth: 05/15/1985. This document is issued by the government.",
    user_document.tags = json.dumps(["identity", "official", "personal"])
    data_response.append(user_document)
    user_document_with_total = UserDocumentsResponseWithTotalCount()
    user_document_with_total.user_documents = data_response
    user_document_with_total.total = 1
    return user_document_with_total
