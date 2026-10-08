import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Entity, EntityType, Relationship, RelationshipType, Resource


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as database_session:
        yield database_session


def test_entity_relationships_and_owned_resources(session):
    parent = Entity(type=EntityType.PERSON, name="Aegon", active_from=27, active_to=37)
    child = Entity(type=EntityType.PERSON, name="Aenys", active_from=7, active_to=42)
    parent.relationships.append(
        Relationship(
            target=child,
            type=RelationshipType.FATHER_OF,
            valid_from=7,
            strength=1.0,
        )
    )
    parent.resources.append(Resource(name="dragon", value="Balerion"))
    session.add(parent)
    session.flush()

    assert parent.relationships[0].target.name == "Aenys"
    assert parent.relationships[0].source.name == "Aegon"
    assert not hasattr(child, "incoming_relationships")
    assert parent.resources[0].owner is parent


def test_relationship_types_are_first_degree_personal_links():
    assert {relationship_type.value for relationship_type in RelationshipType} == {
        "child_of",
        "mother_of",
        "father_of",
        "husband_of",
        "wife_of",
        "lover_of",
        "sibling_of",
    }


@pytest.mark.parametrize(
    "relationship_values",
    [
        {"strength": -0.1},
        {"strength": 1.1},
        {"valid_from": 100, "valid_to": 50},
    ],
)
def test_relationship_constraints(session, relationship_values):
    source = Entity(type=EntityType.PERSON, name="Source")
    target = Entity(type=EntityType.PERSON, name="Target")
    values = {
        "type": RelationshipType.SIBLING_OF,
        "strength": 0.5,
        **relationship_values,
    }
    session.add_all([source, target])
    session.flush()
    session.add(Relationship(source=source, target=target, **values))

    with pytest.raises(IntegrityError):
        session.flush()