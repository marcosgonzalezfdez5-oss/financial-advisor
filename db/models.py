import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class InvestorProfileModel(Base):
    __tablename__ = "investor_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    risk_tolerance: Mapped[str] = mapped_column(String(20), nullable=False)
    investment_horizon_years: Mapped[int] = mapped_column(Integer, nullable=False)
    preferred_regions: Mapped[list] = mapped_column(JSON, nullable=False)
    preferred_sectors: Mapped[list] = mapped_column(JSON, nullable=False)
    dividend_preference: Mapped[bool] = mapped_column(default=False)
    growth_vs_value: Mapped[str] = mapped_column(String(20), nullable=False)
    esg_preference: Mapped[bool] = mapped_column(default=False)
    investor_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contradictions: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    portfolio: Mapped[dict] = mapped_column(JSON, nullable=False)
    risk_summary: Mapped[str] = mapped_column(Text, nullable=False)
    alternatives: Mapped[list] = mapped_column(JSON, default=list)
    uncertainty: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
