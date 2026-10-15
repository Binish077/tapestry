from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Entity, EntityType, Relationship, RelationshipType, Resource


def test_get_tree_returns_people_resources_and_relationships():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    test_session_factory = sessionmaker(bind=engine, class_=Session)

    with test_session_factory() as session:
        parent = Entity(type=EntityType.PERSON, name="Rhaenyra", active_from=97)
        child = Entity(type=EntityType.PERSON, name="Jacaerys", active_from=114)
        place = Entity(type=EntityType.PLACE, name="Dragonstone")
        parent.resources.append(Resource(name="dragon", value="Syrax"))
        parent.relationships.append(
            Relationship(
                target=child,
                type=RelationshipType.MOTHER_OF,
                valid_from=114,
                strength=1.0,
            )
        )
        session.add_all([parent, child, place])
        session.commit()
        parent_id = parent.id
        child_id = child.id

    def override_get_db():
        with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            response = client.get("/api/tree")
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()

    assert response.status_code == 200
    payload = response.json()
    assert {node["name"] for node in payload["nodes"]} == {"Rhaenyra", "Jacaerys"}

    rhaenyra = next(node for node in payload["nodes"] if node["id"] == parent_id)
    assert rhaenyra["resources"] == [{"name": "dragon", "value": "Syrax"}]
    assert len(payload["edges"]) == 1
    edge = payload["edges"][0]
    assert edge["source_id"] == parent_id
    assert edge["target_id"] == child_id
    assert edge["type"] == "parent_child"
    assert edge["relationship_types"] == ["mother_of"]
    assert len(edge["relationship_ids"]) == 1
    assert edge["valid_from"] == 114
    assert edge["valid_to"] is None
    assert edge["strength"] == 1.0