from pydantic import BaseModel
from typing import List


class UserDocumentRequest(BaseModel):
    pages: int = 0
    text: str = ""
    tags: List[str] = []


class UpdateDocumentTagsRequest(BaseModel):
    document_id: int = 0
    tags: List[str] = []


class DeleteDocumentRequest(BaseModel):
    document_id: int = 0
