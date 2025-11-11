import os, asyncio, pytest
from fastapi.testclient import TestClient
from app.main import app, container
from app.db.repository import SynonymRepository, Synonym, SQLModel, create_engine, Session

@pytest.fixture(autouse=True, scope="module")
def temp_sqlite():
    # Use SQLite for tests to avoid SQL Server dependency; schema-compatible subset.
    url = "sqlite:///./test.db"
    eng = create_engine(url)
    SQLModel.metadata.create_all(eng)
    with Session(eng) as s:
        s.add_all([Synonym(word="happy", synonyms="glad,joyful"), Synonym(word="small", synonyms='["tiny","little"]')])
        s.commit()
    # Hot-swap the repository in the app container
    container["repo"] = SynonymRepository(url)
    yield
    os.remove("./test.db")

def test_list_synonyms():
    client = TestClient(app)
    resp = client.get("/synonyms")
    assert resp.status_code == 200
    body = resp.json()
    assert body["cached"] is False
    assert len(body["data"]) >= 2
    # second call must be cached (in-memory by default)
    resp2 = client.get("/synonyms")
    assert resp2.json()["cached"] is True
