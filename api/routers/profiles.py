from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from schemas.investor import InvestorProfileCreate, InvestorProfileResponse

router = APIRouter()


@router.post("/", response_model=InvestorProfileResponse, status_code=201)
async def create_profile(
    payload: InvestorProfileCreate,
    session: AsyncSession = Depends(get_session),
) -> InvestorProfileResponse:
    # TODO: implement
    raise NotImplementedError
