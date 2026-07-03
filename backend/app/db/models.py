from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    hiddify_user_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user")


class Provider(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "providers"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1024))
    category: Mapped[str] = mapped_column(String(64), default="external")
    priority: Mapped[int] = mapped_column(Integer, default=0)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    authentication: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    cache_duration_seconds: Mapped[int] = mapped_column(Integer, default=300)
    update_interval_seconds: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[str] = mapped_column(String(32), default="unknown")
    last_update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    health_score: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scoring_speed: Mapped[float] = mapped_column(Float, default=0.0)
    scoring_healthy_nodes: Mapped[float] = mapped_column(Float, default=0.0)
    scoring_dead_ratio: Mapped[float] = mapped_column(Float, default=0.0)
    scoring_response_time: Mapped[float] = mapped_column(Float, default=0.0)
    scoring_error_rate: Mapped[float] = mapped_column(Float, default=0.0)
    scoring_total: Mapped[float] = mapped_column(Float, default=0.0)

    nodes: Mapped[list["ProviderNode"]] = relationship(back_populates="provider")


class ProviderNode(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "provider_nodes"

    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"), index=True)
    protocol: Mapped[str] = mapped_column(String(32), index=True)
    server: Mapped[str] = mapped_column(String(255), index=True)
    port: Mapped[int] = mapped_column(Integer)
    uuid: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tls: Mapped[bool] = mapped_column(Boolean, default=False)
    reality: Mapped[bool] = mapped_column(Boolean, default=False)
    transport: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sni: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    health: Mapped[str] = mapped_column(String(32), default="unknown")
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    fingerprint: Mapped[str] = mapped_column(String(128), index=True)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)

    provider: Mapped[Provider] = relationship(back_populates="nodes")


class MergedNode(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "merged_nodes"

    subscription_id: Mapped[str] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), index=True)
    provider_node_id: Mapped[str | None] = mapped_column(
        ForeignKey("provider_nodes.id", ondelete="SET NULL"), nullable=True
    )
    source: Mapped[str] = mapped_column(String(32), default="provider")
    node_name: Mapped[str] = mapped_column(String(255))
    protocol: Mapped[str] = mapped_column(String(32))
    fingerprint: Mapped[str] = mapped_column(String(128), index=True)
    rank_score: Mapped[float] = mapped_column(Float, default=0.0)
    final_payload: Mapped[dict] = mapped_column(JSON, default=dict)


class Subscription(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    uuid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    source_hiddify_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    nova_url: Mapped[str] = mapped_column(String(1024), unique=True)
    format: Mapped[str] = mapped_column(String(32), default="base64")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    preview_summary: Mapped[dict] = mapped_column(JSON, default=dict)

    user: Mapped[User] = relationship(back_populates="subscriptions")


class Country(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "countries"

    iso_code: Mapped[str] = mapped_column(String(8), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    flag_emoji: Mapped[str] = mapped_column(String(16))
    continent: Mapped[str | None] = mapped_column(String(64), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)


class HealthCheck(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "health_checks"

    node_fingerprint: Mapped[str] = mapped_column(String(128), index=True)
    check_type: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    packet_loss: Mapped[float] = mapped_column(Float, default=0.0)
    details: Mapped[dict] = mapped_column(JSON, default=dict)


class Rule(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "rules"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    condition: Mapped[dict] = mapped_column(JSON, default=dict)
    action: Mapped[dict] = mapped_column(JSON, default=dict)


class ApiKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "api_keys"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    key_hash: Mapped[str] = mapped_column(String(255), unique=True)
    role: Mapped[str] = mapped_column(String(64), default="readonly")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SchedulerJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "scheduler_jobs"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    cron: Mapped[str] = mapped_column(String(64))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="idle")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class Setting(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(255), unique=True)
    value: Mapped[dict] = mapped_column(JSON, default=dict)
    encrypted: Mapped[bool] = mapped_column(Boolean, default=False)


class Log(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "logs"

    level: Mapped[str] = mapped_column(String(32), index=True)
    logger: Mapped[str] = mapped_column(String(128))
    message: Mapped[str] = mapped_column(Text)
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Backup(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "backups"

    backup_type: Mapped[str] = mapped_column(String(64))
    storage_url: Mapped[str] = mapped_column(String(1024))
    checksum: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="created")
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class AuditLog(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "audit_logs"
    __table_args__ = (UniqueConstraint("actor", "action", "target", "created_at", name="uq_audit_tuple"),)

    actor: Mapped[str] = mapped_column(String(255), index=True)
    action: Mapped[str] = mapped_column(String(255), index=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    changes: Mapped[dict] = mapped_column(JSON, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
