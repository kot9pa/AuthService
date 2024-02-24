from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from base import Base
if TYPE_CHECKING:    
    from api_v1.codes.models import Code


class User(Base):
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    is_active: Mapped[bool]

    created_code_id = mapped_column(Integer, ForeignKey("codes.id"))
    created_code = relationship("Code", foreign_keys="[User.created_code_id]")

    registered_by_code_id = mapped_column(Integer, ForeignKey("codes.id"))
    registered_by_code = relationship("Code", foreign_keys="[User.registered_by_code_id]")
    