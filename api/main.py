from fastapi import FastAPI
from api.routers import profiles, recommendations

app = FastAPI(
    title="Investment Research Agent",
    description="AI-powered ETF and blue-chip stock recommendation system",
    version="0.1.0",
)

app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
