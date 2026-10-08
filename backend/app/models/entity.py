from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum as SQLAlchemyEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.relationship import Relationship
    from app.models.resource import Resource


class EntityType(str, Enum):
    PERSON = "person"
    PLACE = "place"


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = (
        CheckConstraint(
            "active_to IS NULL OR active_from IS NULL OR active_to >= active_from",
            name="ck_entities_active_years",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[EntityType] = mapped_column(
        SQLAlchemyEnum(
            EntityType,
            name="entity_type",
            native_enum=False,
            values_callable=lambda enum: [member.value for member in enum],
            create_constraint=True,
        ),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    active_from: Mapped[Optional[int]] = mapped_column(Integer)
    active_to: Mapped[Optional[int]] = mapped_column(Integer)

    relationships: Mapped[list[Relationship]] = orm_relationship(
        back_populates="source",
        foreign_keys="Relationship.source_id",
        cascade="all, delete-orphan",
    )
    resources: Mapped[list[Resource]] = orm_relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )
