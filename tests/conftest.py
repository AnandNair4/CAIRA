import pytest


@pytest.fixture(scope="session", autouse=True)
def seeded_db():
    from db.seed import seed

    seed()
    yield
