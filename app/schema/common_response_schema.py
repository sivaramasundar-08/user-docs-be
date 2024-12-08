from typing import Any, Optional

import pydantic


class CommonResponseSchema(pydantic.BaseModel):
    status: Optional[str]
    message: Optional[str]


class ErrorResponseSchema(CommonResponseSchema):
    error_detail: Optional[str]


class DataResponseSchema(CommonResponseSchema):
    data: Optional[Any]

