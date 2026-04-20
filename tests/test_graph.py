from agents.state import AgentState


def make_empty_state() -> AgentState:
    return AgentState(
        investor_profile=None,
        market_data={},
        portfolio_draft=None,
        recommendation=None,
        errors=[],
        requires_human_review=False,
        trace_id="test-trace-001",
    )


def test_initial_state_is_valid() -> None:
    state = make_empty_state()
    assert state["investor_profile"] is None
    assert state["errors"] == []
    assert state["trace_id"] == "test-trace-001"
