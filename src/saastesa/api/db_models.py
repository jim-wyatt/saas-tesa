from datetime import datetime
from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SecurityFindingRecord(Base):
    __tablename__ = "security_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    finding_uid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    standard: Mapped[str] = mapped_column(String(32))
    schema_version: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    severity_id: Mapped[int] = mapped_column(Integer)
    severity: Mapped[str] = mapped_column(String(32))
    risk_score: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(1024))
    category_name: Mapped[str] = mapped_column(String(128))
    class_name: Mapped[str] = mapped_column(String(128))
    type_name: Mapped[str] = mapped_column(String(128))
    domain: Mapped[str] = mapped_column(String(64), index=True)
    activity_name: Mapped[str] = mapped_column(String(64))
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(128), index=True)

    resource_uid: Mapped[str] = mapped_column(String(256))
    resource_name: Mapped[str] = mapped_column(String(256))
    resource_type: Mapped[str] = mapped_column(String(128))
    resource_platform: Mapped[str] = mapped_column(String(128))

    references_json: Mapped[dict[str, object]] = mapped_column(JSON)
    raw_data: Mapped[dict[str, object]] = mapped_column(JSON)
