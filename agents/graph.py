from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.profile_agent import run_profile_agent
from agents.research_agent import run_research_agent
from agents.portfolio_agent import run_portfolio_agent


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("profile", run_profile_agent)
    graph.add_node("research", run_research_agent)
    graph.add_node("portfolio", run_portfolio_agent)

    graph.set_entry_point("profile")
    graph.add_edge("profile", "research")
    graph.add_edge("research", "portfolio")
    graph.add_edge("portfolio", END)

    return graph.compile()


agent_graph = build_graph()
