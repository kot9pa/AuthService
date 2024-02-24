from datetime import date
from pydantic import BaseModel, ConfigDict


class CodeBase(BaseModel):
    code: str
    expire: date

class Code(CodeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CodeCreate(CodeBase):
    pass
