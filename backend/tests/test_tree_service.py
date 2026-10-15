from app.models import Relationship, RelationshipType
from app.schemas.tree import TreeEdgeType
from app.services.relationship_normalizer import normalize_relationships


def test_reciprocal_spouse_relationships_become_one_marriage_edge():
    relationships = [
        Relationship(
            id=12,
            source_id=20,
            target_id=10,
            type=RelationshipType.WIFE_OF,
            valid_from=120,
            valid_to=130,
            strength=0.75,
        ),
        Relationship(
            id=11,
            source_id=10,
            target_id=20,
            type=RelationshipType.HUSBAND_OF,
            valid_from=120,
            valid_to=130,
            strength=0.75,
        ),
    ]

    edges = normalize_relationships(relationships)

    assert len(edges) == 1
    edge = edges[0]
    assert edge.id == 11
    assert edge.relationship_ids == [11, 12]
    assert edge.source_id == 10
    assert edge.target_id == 20
    assert edge.type == TreeEdgeType.MARRIAGE
    assert set(edge.relationship_types) == {
        RelationshipType.HUSBAND_OF,
        RelationshipType.WIFE_OF,
    }


def test_child_of_is_reoriented_parent_to_child():
    relationship = Relationship(
        id=13,
        source_id=20,
        target_id=10,
        type=RelationshipType.CHILD_OF,
        valid_from=120,
        valid_to=130,
        strength=1.0,
    )

    edges = normalize_relationships([relationship])

    assert len(edges) == 1
    assert edges[0].source_id == 10
    assert edges[0].target_id == 20
    assert edges[0].type == TreeEdgeType.PARENT_CHILD
    assert edges[0].relationship_types == [RelationshipType.CHILD_OF]


def test_one_sided_wife_relationship_still_produces_marriage_edge():
    relationship = Relationship(
        id=14,
        source_id=20,
        target_id=10,
        type=RelationshipType.WIFE_OF,
        valid_from=None,
        valid_to=None,
        strength=0.75,
    )

    edges = normalize_relationships([relationship])

    assert len(edges) == 1
    assert edges[0].source_id == 10
    assert edges[0].target_id == 20
    assert edges[0].type == TreeEdgeType.MARRIAGE
    assert edges[0].relationship_ids == [14]