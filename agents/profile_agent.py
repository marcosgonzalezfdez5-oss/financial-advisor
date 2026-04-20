import json
import logging

import anthropic

from agents.state import AgentState
from config.settings import settings
from schemas.investor import GrowthVsValue, InvestorProfile, RiskTolerance

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

_INVESTOR_TYPE_MAP = {
    (RiskTolerance.LOW, True): "Conservative Income",
    (RiskTolerance.LOW, False): "Conservative Growth",
    (RiskTolerance.MEDIUM, True): "Balanced Income",
    (RiskTolerance.MEDIUM, False): "Balanced Growth",
    (RiskTolerance.HIGH, True): "Growth Income",
    (RiskTolerance.HIGH, False): "Aggressive Growth",
}


def _classify_investor_type(profile: InvestorProfile) -> str:
    return _INVESTOR_TYPE_MAP[(profile.risk_tolerance, profile.dividend_preference)]


def _detect_contradictions(profile: InvestorProfile) -> list[str]:
    prompt = f"""You are a financial analyst reviewing an investor profile for internal consistency.

Profile:
{json.dumps(profile.model_dump(mode="json"), indent=2)}

Identify any contradictions between the stated preferences. Focus on:
- Risk tolerance vs growth/value preference (e.g., low risk + aggressive growth = contradiction)
- Investment horizon vs risk tolerance (e.g., 1-year horizon + high risk = concern)
- Dividend preference vs growth orientation (e.g., dividend preference + pure growth = mild tension)
- Budget size vs diversification needs

Respond ONLY with a JSON array of plain-English contradiction strings.
If no contradictions, return an empty array [].
Maximum 3 items. Be concise.

Example: ["Low risk tolerance conflicts with aggressive growth preference."]
"""

    try:
        response = _client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        # Extract JSON array from response
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end]) if start != -1 else []
    except Exception as exc:
        logger.warning("Contradiction detection failed: %s", exc)
        return []


def run_profile_agent(state: AgentState) -> AgentState:
    profile = state["investor_profile"]
    if profile is None:
        return {**state, "errors": state["errors"] + ["ProfileAgent: no investor_profile in state"]}

    investor_type = _classify_investor_type(profile)
    contradictions = _detect_contradictions(profile)

    requires_human_review = len(contradictions) > 0

    enriched = profile.model_copy(update={
        "investor_type": investor_type,
        "contradictions": contradictions,
    })

    logger.info(
        "ProfileAgent: classified as '%s', %d contradiction(s)",
        investor_type,
        len(contradictions),
    )

    return {
        **state,
        "investor_profile": enriched,
        "requires_human_review": requires_human_review,
    }
