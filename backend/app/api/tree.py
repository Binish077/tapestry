from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models import Entity, EntityType, Relationship
from app.schemas.tree import TreeNode, TreeResource, TreeResponse
from app.services.relationship_normalizer import normalize_relationships

router = APIRouter()


@router.get("/tree", response_model=TreeResponse)
def get_tree(session: Annotated[Session, Depends(get_db)]) -> TreeResponse:
    people = session.scalars(
        select(Entity)
        .where(Entity.type == EntityType.PERSON)
        .options(selectinload(Entity.resources))
        .order_by(Entity.name)
    ).all()
    person_ids = {person.id for person in people}

    relationships = []
    if person_ids:
        relationships = session.scalars(
            select(Relationship)
            .where(
                Relationship.source_id.in_(person_ids),
                Relationship.target_id.in_(person_ids),
            )
            .order_by(Relationship.id)
        ).all()

    return TreeResponse(
        nodes=[
            TreeNode(
                id=person.id,
                name=person.name,
                active_from=person.active_from,
                active_to=person.active_to,
                resources=[
                    TreeResource(name=resource.name, value=resource.value)
                    for resource in person.resources
                ],
            )
            for person in people
        ],
        edges=normalize_relationships(relationships),
    )