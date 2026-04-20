import asyncio
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from agents.graph import agent_graph
from agents.state import AgentState
from db.models import RecommendationModel
from db.repository import InvestorProfileRepository, RecommendationRepository
from db.session import get_session
from schemas.investor import InvestorProfile
from schemas.recommendation import RecommendationRequest, RecommendationResponse

router = APIRouter()


def _build_initial_state(profile: InvestorProfile) -> AgentState:
    return AgentState(
        investor_profile=profile,
        market_data={},
        portfolio_draft=None,
        recommendation=None,
        errors=[],
        requires_human_review=False,
        trace_id=str(uuid.uuid4()),
    )


@router.post("/", response_model=RecommendationResponse, status_code=201)
async def create_recommendation(
    payload: RecommendationRequest,
    session: AsyncSession = Depends(get_session),
) -> RecommendationResponse:
    profile_repo = InvestorProfileRepository(session)
    profile_model = await profile_repo.get_by_id(payload.profile_id)
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Investor profile not found")

    profile = InvestorProfile(
        id=profile_model.id,
        budget=profile_model.budget,
        currency=profile_model.currency,
        risk_tolerance=profile_model.risk_tolerance,
        investment_horizon_years=profile_model.investment_horizon_years,
        preferred_regions=profile_model.preferred_regions,
        preferred_sectors=profile_model.preferred_sectors,
        dividend_preference=profile_model.dividend_preference,
        growth_vs_value=profile_model.growth_vs_value,
        esg_preference=profile_model.esg_preference,
        investor_type=profile_model.investor_type,
        contradictions=profile_model.contradictions,
    )

    initial_state = _build_initial_state(profile)

    # Run the sync LangGraph graph in a thread to avoid blocking the event loop
    final_state: AgentState = await asyncio.to_thread(agent_graph.invoke, initial_state)

    recommendation = final_state.get("recommendation")
    if recommendation is None:
        errors = final_state.get("errors", [])
        raise HTTPException(
            status_code=500,
            detail={"message": "Agent pipeline failed to produce a recommendation", "errors": errors},
        )

    rec_repo = RecommendationRepository(session)
    await rec_repo.create(
        RecommendationModel(
            id=recommendation.id,
            profile_id=recommendation.profile_id,
            portfolio=[h.model_dump(mode="json") for h in recommendation.portfolio],
            risk_summary=recommendation.risk_summary,
            alternatives=recommendation.alternatives,
            uncertainty=recommendation.uncertainty.model_dump(mode="json"),
        )
    )

    return RecommendationResponse.model_validate(recommendation)
