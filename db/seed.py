"""Seed the SQLite database with the previously hardcoded mock SOC data."""

from sqlalchemy import select

from db.database import Base, get_engine, get_session_factory
from db.models import AssetRecord, LogEntry, ThreatIntelRecord

LOG_ROWS = [
    ("jdoe", "login from 203.0.113.5", "09:14:00"),
    ("jdoe", "password reset requested", "09:15:02"),
    ("admin_user", "routine database query", "09:00:00"),
]

INTEL_ROWS = [
    ("203.0.113.5", True, 0.72),
    ("8.8.8.8", False, 0.0),
]

ASSET_ROWS = [
    ("jdoe", "standard_user", 0.3),
    ("admin_user", "database_admin", 0.9),
]


def seed(db_url: str = "sqlite:///mock_soc.db") -> None:
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    Session = get_session_factory(db_url)

    with Session() as session:
        for user, event, time_ in LOG_ROWS:
            if not session.scalars(
                select(LogEntry).where(LogEntry.user == user, LogEntry.event == event)
            ).first():
                session.add(LogEntry(user=user, event=event, time=time_))

        for ip, malicious, confidence in INTEL_ROWS:
            if not session.scalars(
                select(ThreatIntelRecord).where(ThreatIntelRecord.ip == ip)
            ).first():
                session.add(
                    ThreatIntelRecord(ip=ip, malicious=malicious, confidence=confidence)
                )

        for user, role, criticality in ASSET_ROWS:
            if not session.scalars(
                select(AssetRecord).where(AssetRecord.user == user)
            ).first():
                session.add(AssetRecord(user=user, role=role, criticality=criticality))

        session.commit()


if __name__ == "__main__":
    seed()
    print("Seeded mock_soc.db")
