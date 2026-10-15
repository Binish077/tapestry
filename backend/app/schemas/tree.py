from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models import RelationshipType


class TreeEdgeType(str, Enum):
    PARENT_CHILD = "parent_child"
    MARRIAGE = "marriage"
    LOVER = "lover"
    SIBLING = "sibling"


class TreeResource(BaseModel):
    name: str
    value: str


class TreeNode(BaseModel):
    id: int
    name: str
    active_from: Optional[int]  # noqa: UP045
    active_to: Optional[int]  # noqa: UP045
    resources: list[TreeResource]


class TreeEdge(BaseModel):
    id: int
    relationship_ids: list[int]
    source_id: int
    target_id: int
    type: TreeEdgeType
    relationship_types: list[RelationshipType]
    valid_from: Optional[int]  # noqa: UP045
    valid_to: Optional[int]  # noqa: UP045
    strength: float


class TreeResponse(BaseModel):
    nodes: list[TreeNode]
    edges: list[TreeEdge]