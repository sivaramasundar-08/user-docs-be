from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, VARCHAR
from typing import Optional


class CommonInfoModel:
    __abstract__ = True

    is_active: Optional[bool] = Column(TINYINT(1), nullable=True)
    created_at: Optional[int] = Column(BIGINT(20), nullable=True)
    updated_at: Optional[int] = Column(BIGINT(20), nullable=True)
    user_email: Optional[str] = Column(VARCHAR(255), nullable=True)
