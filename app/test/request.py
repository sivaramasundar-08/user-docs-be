from app.schema import (
    FilterRequestSchema,
    UserDocumentRequest,
    UpdateDocumentTagsRequest,
    DeleteDocumentRequest
)


class RequestBody:
    filter_request = FilterRequestSchema()

    upload_document_request = UserDocumentRequest()
    upload_document_request.pages = 10,
    upload_document_request.text = "This is a sample ID card document. ID Number: 987654321, Date of Birth: 05/15/1985. This document is issued by the government.",
    upload_document_request.tags = ["identity", "official", "personal"]

    update_document_tags_request = UpdateDocumentTagsRequest()
    update_document_tags_request.document_id = 1
    update_document_tags_request.tags = ["updated", "personal", "important"]

    delete_document_request = DeleteDocumentRequest()
    delete_document_request.document_id = 1

