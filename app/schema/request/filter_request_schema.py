from typing import Any, List, Optional

import pydantic
from pydantic import Field


class FilterSchema(pydantic.BaseModel):
    field: Optional[str] = ""
    values: Optional[Any] = None
    operator: Optional[str] = ""


class SortSchema(pydantic.BaseModel):
    field: Optional[str] = ""
    order: Optional[str] = ""


class PageInfoSchema(pydantic.BaseModel):
    start: Optional[int] = 0
    rows: Optional[int] = 0


class FilterRequestSchema(pydantic.BaseModel):
    search_key: Optional[str] = ""
    search_text: Optional[str] = ""
    filters: Optional[List[FilterSchema]] = []
    sort: Optional[List[SortSchema]] = []
    page_info: Optional[PageInfoSchema] = Field(
        PageInfoSchema(start=0, rows=0), alias="pageInfo", title="pageInfo"
    )

