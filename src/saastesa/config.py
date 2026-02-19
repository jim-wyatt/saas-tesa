from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    environment: str
    organization: str
    log_level: str


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("TESA_ENV", "development"),
        organization=os.getenv("TESA_ORGANIZATION", "unknown-org"),
        log_level=os.getenv("TESA_LOG_LEVEL", "INFO"),
    )
