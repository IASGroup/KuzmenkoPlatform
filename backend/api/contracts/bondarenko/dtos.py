import pydantic
import typing

class ParseTaskDto(pydantic.BaseModel):
    id : str
    theme_uri: str
    theme_name: str
    from_page: int
    to_page: int
    current_page: int
    current_article: int
    is_done: bool
    is_running: bool

class CreateParseTaskRequestDto(pydantic.BaseModel):
    theme_uri: str
    theme_name: str
    from_page: int
    to_page: int