import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import InvestorProfileModel
from db.repository import InvestorProfileRepository
from db.session import get_session
from schemas.investor import InvestorProfileCreate, InvestorProfileResponse

router = APIRouter()


@router.post("/", response_model=InvestorProfileResponse, status_code=201)
async def create_profile(
    payload: InvestorProfileCreate,
    session: AsyncSession = Depends(get_session),
) -> InvestorProfileResponse:
    profile_id = uuid.uuid4()
    model = InvestorProfileModel(
        id=profile_id,
        budget=payload.budget,
        currency=payload.currency,
        risk_tolerance=payload.risk_tolerance,
        investment_horizon_years=payload.investment_horizon_years,
        preferred_regions=payload.preferred_regions,
        preferred_sectors=payload.preferred_sectors,
        dividend_preference=payload.dividend_preference,
        growth_vs_value=payload.growth_vs_value,
        esg_preference=payload.esg_preference,
        contradictions=[],
    )
    repo = InvestorProfileRepository(session)
    saved = await repo.create(model)

    return InvestorProfileResponse(
        id=saved.id,
        budget=saved.budget,
        currency=saved.currency,
        risk_tolerance=saved.risk_tolerance,
        investment_horizon_years=saved.investment_horizon_years,
        preferred_regions=saved.preferred_regions,
        preferred_sectors=saved.preferred_sectors,
        dividend_preference=saved.dividend_preference,
        growth_vs_value=saved.growth_vs_value,
        esg_preference=saved.esg_preference,
        investor_type=saved.investor_type,
        contradictions=saved.contradictions,
    )


@router.get("/{profile_id}", response_model=InvestorProfileResponse)
async def get_profile(
    profile_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> InvestorProfileResponse:
    repo = InvestorProfileRepository(session)
    model = await repo.get_by_id(profile_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return InvestorProfileResponse(
        id=model.id,
        budget=model.budget,
        currency=model.currency,
        risk_tolerance=model.risk_tolerance,
        investment_horizon_years=model.investment_horizon_years,
        preferred_regions=model.preferred_regions,
        preferred_sectors=model.preferred_sectors,
        dividend_preference=model.dividend_preference,
        growth_vs_value=model.growth_vs_value,
        esg_preference=model.esg_preference,
        investor_type=model.investor_type,
        contradictions=model.contradictions,
    )
