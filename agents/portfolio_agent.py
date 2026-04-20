from agents.state import AgentState
from core.allowlist import validate_portfolio


def run_portfolio_agent(state: AgentState) -> AgentState:
    # TODO: build portfolio draft, call Claude with injected market data,
    # validate output through allowlist before writing to state
    return state
