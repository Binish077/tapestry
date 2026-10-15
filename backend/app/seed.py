import json
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Entity, EntityType, Relationship, RelationshipType, Resource


SEED_FILE = Path(__file__).resolve().parents[1] / "data" / "seed.json"


def load_seed_data(session: Session, data: dict[str, Any]) -> dict[str, int]:
    entities: dict[str, Entity] = {}
    counts = {"entities_added": 0, "entities_updated": 0, "relationships_added": 0,
              "relationships_updated": 0, "resources_added": 0, "resources_updated": 0}

    for entity_data in data["entities"]:
        entity_type = EntityType(entity_data["type"])
        existing = session.scalars(
            select(Entity).where(
                Entity.type == entity_type,
                Entity.name == entity_data["name"],
            )
        ).all()
        if len(existing) > 1:
            raise ValueError(f"Multiple entities match seed key {entity_data['key']!r}")

        if existing:
            entity = existing[0]
            counts["entities_updated"] += 1
        else:
            entity = Entity(type=entity_type, name=entity_data["name"])
            session.add(entity)
            counts["entities_added"] += 1

        entity.active_from = entity_data["active_from"]
        entity.active_to = entity_data["active_to"]
        session.flush()
        entities[entity_data["key"]] = entity

    for relationship_data in data["relationships"]:
        source = entities[relationship_data["source"]]
        target = entities[relationship_data["target"]]
        relationship_type = RelationshipType(relationship_data["type"])
        valid_from = relationship_data["valid_from"]
        valid_to = relationship_data["valid_to"]
        existing = session.scalars(
            select(Relationship).where(
                Relationship.source_id == source.id,
                Relationship.target_id == target.id,
                Relationship.type == relationship_type,
                Relationship.valid_from == valid_from,
                Relationship.valid_to == valid_to,
            )
        ).all()
        if len(existing) > 1:
            raise ValueError(
                f"Duplicate database relationships match {source.name} -> {target.name}"
            )

        if existing:
            relationship = existing[0]
            counts["relationships_updated"] += 1
        else:
            relationship = Relationship(
                source=source,
                target=target,
                type=relationship_type,
                valid_from=valid_from,
                valid_to=valid_to,
                strength=relationship_data["strength"],
            )
            session.add(relationship)
            counts["relationships_added"] += 1

        relationship.strength = relationship_data["strength"]

    for resource_data in data["resources"]:
        owner = entities[resource_data["owner"]]
        existing = session.scalars(
            select(Resource).where(
                Resource.owner_id == owner.id,
                Resource.name == resource_data["name"],
            )
        ).all()
        if len(existing) > 1:
            raise ValueError(
                f"Duplicate {resource_data['name']!r} resources for {owner.name}"
            )

        if existing:
            resource = existing[0]
            counts["resources_updated"] += 1
        else:
            resource = Resource(owner=owner, name=resource_data["name"], value="")
            session.add(resource)
            counts["resources_added"] += 1

        resource.value = resource_data["value"]

    session.flush()
    return counts


def main() -> None:
    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    with SessionLocal.begin() as session:
        counts = load_seed_data(session, data)

    for name, count in counts.items():
        print(f"{name}: {count}")


if __name__ == "__main__":
    main()