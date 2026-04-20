from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import InvestorProfileModel, RecommendationModel


class InvestorProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, model: InvestorProfileModel) -> InvestorProfileModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_id(self, profile_id: UUID) -> InvestorProfileModel | None:
        result = await self.session.execute(
            select(InvestorProfileModel).where(InvestorProfileModel.id == profile_id)
        )
        return result.scalar_one_or_none()


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, model: RecommendationModel) -> RecommendationModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_profile_id(self, profile_id: UUID) -> list[RecommendationModel]:
        result = await self.session.execute(
            select(RecommendationModel)
            .where(RecommendationModel.profile_id == profile_id)
            .order_by(RecommendationModel.created_at.desc())
        )
        return list(result.scalars().all())
