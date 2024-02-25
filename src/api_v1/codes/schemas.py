from datetime import date
from pydantic import BaseModel, ConfigDict


class CodeBase(BaseModel):
    code: str
    expire: date

class Code(CodeBase):
    id: int

class CodeCreate(CodeBase):
    pass
