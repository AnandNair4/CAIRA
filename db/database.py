from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import PROJECT_ROOT, get_settings


class Base(DeclarativeBase):
    pass


def resolve_db_url(db_url: str) -> str:
    prefix = "sqlite:///"
    if db_url.startswith(prefix):
        path = Path(db_url[len(prefix):])
        if not path.is_absolute():
            return prefix + str(PROJECT_ROOT / path)
    return db_url


@lru_cache(maxsize=8)
def get_engine(db_url: str | None = None):
    db_url = db_url or get_settings().db.url
    return create_engine(resolve_db_url(db_url), echo=False)


@lru_cache(maxsize=8)
def get_session_factory(db_url: str | None = None):
    return sessionmaker(bind=get_engine(db_url), expire_on_commit=False)
