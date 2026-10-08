from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum as SQLAlchemyEnum, Float, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.entity import Entity


class RelationshipType(str, Enum):
    CHILD_OF = "child_of"
    MOTHER_OF = "mother_of"
    FATHER_OF = "father_of"
    HUSBAND_OF = "husband_of"
    WIFE_OF = "wife_of"
    LOVER_OF = "lover_of"
    SIBLING_OF = "sibling_of"


class Relationship(Base):
    __tablename__ = "relationships"
    __table_args__ = (
        CheckConstraint(
            "strength >= 0 AND strength <= 1",
            name="ck_relationships_strength_range",
        ),
        CheckConstraint(
            "valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from",
            name="ck_relationships_valid_years",
        ),
        Index("ix_relationships_source_type", "source_id", "type"),
        Index("ix_relationships_target_type", "target_id", "type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), nullable=False
    )
    target_id: Mapped[int] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[RelationshipType] = mapped_column(
        SQLAlchemyEnum(
            RelationshipType,
            name="relationship_type",
            native_enum=False,
            values_callable=lambda enum: [member.value for member in enum],
            create_constraint=True,
        ),
        nullable=False,
        index=True,
    )
    valid_from: Mapped[Optional[int]] = mapped_column(Integer)
    valid_to: Mapped[Optional[int]] = mapped_column(Integer)
    strength: Mapped[float] = mapped_column(Float, nullable=False)

    source: Mapped[Entity] = orm_relationship(
        back_populates="relationships",
        foreign_keys=[source_id],
    )
    target: Mapped[Entity] = orm_relationship(foreign_keys=[target_id])
