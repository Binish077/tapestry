from collections import defaultdict
from collections.abc import Iterable

from app.models import Relationship, RelationshipType
from app.schemas.tree import TreeEdge, TreeEdgeType


def normalize_relationships(relationships: Iterable[Relationship]) -> list[TreeEdge]:
    edges: list[TreeEdge] = []
    marriages: defaultdict[tuple[int, int], list[Relationship]] = defaultdict(list)

    for relationship in relationships:
        if relationship.type in (RelationshipType.HUSBAND_OF, RelationshipType.WIFE_OF):
            pair = tuple(sorted((relationship.source_id, relationship.target_id)))
            marriages[pair].append(relationship)
            continue

        if relationship.type in (
            RelationshipType.FATHER_OF,
            RelationshipType.MOTHER_OF,
        ):
            source_id = relationship.source_id
            target_id = relationship.target_id
            edge_type = TreeEdgeType.PARENT_CHILD
        elif relationship.type == RelationshipType.CHILD_OF:
            source_id = relationship.target_id
            target_id = relationship.source_id
            edge_type = TreeEdgeType.PARENT_CHILD
        elif relationship.type == RelationshipType.LOVER_OF:
            source_id = relationship.source_id
            target_id = relationship.target_id
            edge_type = TreeEdgeType.LOVER
        elif relationship.type == RelationshipType.SIBLING_OF:
            source_id = relationship.source_id
            target_id = relationship.target_id
            edge_type = TreeEdgeType.SIBLING
        else:
            continue

        edges.append(
            TreeEdge(
                id=relationship.id,
                relationship_ids=[relationship.id],
                source_id=source_id,
                target_id=target_id,
                type=edge_type,
                relationship_types=[relationship.type],
                valid_from=relationship.valid_from,
                valid_to=relationship.valid_to,
                strength=relationship.strength,
            )
        )

    for pair, pair_relationships in marriages.items():
        husband_record = next(
            (
                relationship
                for relationship in pair_relationships
                if relationship.type == RelationshipType.HUSBAND_OF
            ),
            None,
        )
        wife_record = next(
            (
                relationship
                for relationship in pair_relationships
                if relationship.type == RelationshipType.WIFE_OF
            ),
            None,
        )

        if husband_record is not None:
            source_id = husband_record.source_id
            target_id = husband_record.target_id
        elif wife_record is not None:
            source_id = wife_record.target_id
            target_id = wife_record.source_id
        else:
            continue

        valid_starts = [
            relationship.valid_from
            for relationship in pair_relationships
            if relationship.valid_from is not None
        ]
        valid_ends = [
            relationship.valid_to
            for relationship in pair_relationships
            if relationship.valid_to is not None
        ]
        relationship_types = sorted(
            {relationship.type for relationship in pair_relationships},
            key=lambda relationship_type: relationship_type.value,
        )

        edges.append(
            TreeEdge(
                id=min(relationship.id for relationship in pair_relationships),
                relationship_ids=sorted(
                    relationship.id for relationship in pair_relationships
                ),
                source_id=source_id,
                target_id=target_id,
                type=TreeEdgeType.MARRIAGE,
                relationship_types=relationship_types,
                valid_from=min(valid_starts) if valid_starts else None,
                valid_to=(
                    None
                    if any(relationship.valid_to is None for relationship in pair_relationships)
                    else max(valid_ends)
                ),
                strength=max(relationship.strength for relationship in pair_relationships),
            )
        )

    return sorted(edges, key=lambda edge: edge.id)