from typing import Optional

from pydantic import BaseModel

from app.models import RelationshipType


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
    source_id: int
    target_id: int
    type: RelationshipType
    valid_from: Optional[int]  # noqa: UP045
    valid_to: Optional[int]  # noqa: UP045
    strength: float


class TreeResponse(BaseModel):
    nodes: list[TreeNode]
    edges: list[TreeEdge]