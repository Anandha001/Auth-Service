from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
