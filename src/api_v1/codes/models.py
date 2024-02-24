from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from base import Base
if TYPE_CHECKING:    
    from api_v1.users.models import User

class Code(Base):
    code: Mapped[str]
    expire: Mapped[date] = mapped_column(server_default=func.current_date())

    created_by_id: Mapped[int]
