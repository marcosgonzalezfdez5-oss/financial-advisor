from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from schemas.recommendation import RecommendationRequest, RecommendationResponse

router = APIRouter()


@router.post("/", response_model=RecommendationResponse, status_code=201)
async def create_recommendation(
    payload: RecommendationRequest,
    session: AsyncSession = Depends(get_session),
) -> RecommendationResponse:
    # TODO: implement
    raise NotImplementedError
