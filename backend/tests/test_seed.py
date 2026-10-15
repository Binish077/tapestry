import json
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Entity, Relationship, Resource
from app.seed import SEED_FILE, load_seed_data


def test_seed_is_repeatable():
    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        first_counts = load_seed_data(session, data)
        session.commit()
        second_counts = load_seed_data(session, data)
        session.commit()

        assert first_counts["entities_added"] == len(data["entities"])
        assert first_counts["relationships_added"] == len(data["relationships"])
        assert first_counts["resources_added"] == len(data["resources"])
        assert second_counts["entities_added"] == 0
        assert second_counts["relationships_added"] == 0
        assert second_counts["resources_added"] == 0
        assert session.scalar(select(func.count()).select_from(Entity)) == len(data["entities"])
        assert session.scalar(select(func.count()).select_from(Relationship)) == len(
            data["relationships"]
        )
        assert session.scalar(select(func.count()).select_from(Resource)) == len(
            data["resources"]
        )