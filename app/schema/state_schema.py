import pydantic


class StateSchema(pydantic.BaseModel):
    # Remove values afterwards
    user_name: str = ""
    email_id: str = ""
    request_id: str = ""
