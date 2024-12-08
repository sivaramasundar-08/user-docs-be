from starlette.datastructures import State

from app.schema import StateSchema


def state_parser(state: State) -> StateSchema:
    state_value_dict = state.__dict__.get("_state", {})
    state_schema = StateSchema.parse_obj(state_value_dict)
    return state_schema
