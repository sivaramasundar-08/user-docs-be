import pydantic


class UserDocumentsResponse(pydantic.BaseModel):
    id: int = 0
    created_at: int = 0
    updated_at: int = 0
    user_email: str = ""
    pages: int = 0
    text: str = ""
    tags: list = []
    document_type: str = ""


class UserDocumentsResponseWithTotalCount(pydantic.BaseModel):
    user_documents: list[UserDocumentsResponse] = []
    total: int = 0
