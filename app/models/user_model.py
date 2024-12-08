from app.models.common_info_model import CommonInfoModel
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, LONGTEXT
from sqlalchemy import Column
from typing import Optional


class UserDocumentModel(CommonInfoModel):
    id: Optional[int] = Column(BIGINT(20), primary_key=True, autoincrement=True)
    pages: Optional[int] = Column(BIGINT(20), nullable=True)
    text: Optional[str] = Column(LONGTEXT, nullable=True)
    tags: Optional[str] = Column(LONGTEXT, nullable=True)
    document_type: Optional[str] = Column(VARCHAR(255), nullable=True)
