from typing import Optional
from app.config.constants import Constants
from fastapi import HTTPException, status


def identify_document_type(text: str) -> Optional[str]:
    text = text.lower().translate(str.maketrans("", "", " _-"))
    for doc_type, keywords in Constants.document_keywords.items():
        for keyword in keywords:
            keyword_check = keyword.lower().replace(" ", "")
            if keyword_check in text:
                return doc_type
    return "invalid"


def some_protected_function():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access",
    )
