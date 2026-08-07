from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


class DecisionThresholds(BaseModel):
    malicious: float
    uncertain: float


class AgentSettings(BaseModel):
    model: str
    max_iterations: int


class TrustWeights(BaseModel):
    verified: float
    corroborated: float
    untrusted: float


class DBSettings(BaseModel):
    url: str


class LoggingSettings(BaseModel):
    level: str


class Settings(BaseModel):
    decision_thresholds: DecisionThresholds
    agent: AgentSettings
    trust_weights: TrustWeights
    db: DBSettings
    logging: LoggingSettings


def load_settings(path: Path | str = CONFIG_PATH) -> Settings:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return Settings(**raw)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
