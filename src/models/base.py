from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        list[str]: JSONB,
        list[dict[str, Any]]: JSONB,
        dict[str, Any]: JSONB,
    }

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    def __repr__(self) -> str:
        return f"{type(self)} id: {self.id}"
