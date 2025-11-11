from __future__ import annotations
from typing import Iterable, TypedDict
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Synonym(SQLModel, table=True):
    __tablename__ = "synonyms"  # id, word, synonyms (comma or json array string)
    id: int | None = Field(default=None, primary_key=True)
    word: str
    synonyms: str

class SynonymRecord(TypedDict):
    id: int
    word: str
    synonyms: list[str]

def _parse_synonyms(raw: str) -> list[str]:
    # Accept comma-separated or JSON; be tolerant in prototype
    import json
    raw = raw.strip()
    if not raw:
        return []
    try:
        v = json.loads(raw)
        if isinstance(v, list):
            return [str(x) for x in v]
    except Exception:
        pass
    return [s.strip() for s in raw.split(",") if s.strip()]

class SynonymRepository:
    def __init__(self, engine_url: str) -> None:
        self._engine = create_engine(engine_url, pool_pre_ping=True, pool_size=10, max_overflow=20)

    def list_all(self) -> Iterable[SynonymRecord]:
        with Session(self._engine) as session:
            rows = session.exec(select(Synonym)).all()
            for r in rows:
                yield {"id": r.id or -1, "word": r.word, "synonyms": _parse_synonyms(r.synonyms)}

    def dispose(self) -> None:
        self._engine.dispose()
