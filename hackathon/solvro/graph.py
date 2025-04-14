from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import CompiledGraph
from loguru import logger

from .agents.graph_analyst import create_graph_analyst_agent
from .state import HackathonState


# def improve_hypothesis(
#     state: HypgenState,
# ) -> Literal["hypothesis_refiner", "summary_agent"]:
#     if state["iteration"] > 3:
#         logger.info("Iteration limit reached after {} iterations", state["iteration"])
#         return "summary_agent"
#     if "ACCEPT" in state["critique"]:
#         logger.info("Hypothesis accepted after {} iterations", state["iteration"])
#         return "summary_agent"
#     else:
#         logger.info("Hypothesis rejected after {} iterations", state["iteration"])
#         return "hypothesis_refiner"


def create_hackathon_graph() -> CompiledGraph:
    graph = StateGraph(HackathonState)

    # Add nodes with specialized agents
    graph.add_node("graph_analyst", create_graph_analyst_agent("reasoning")["agent"])
    # graph.add_node(
    #     "hypothesis_generator", create_hypothesis_generator_agent("small")["agent"]
    # )
    # graph.add_node(
    #     "hypothesis_refiner", create_hypothesis_refiner_agent("small")["agent"]
    # )
    # graph.add_node("literature_agent", create_literature_agent("small")["agent"])
    # graph.add_node("novelty_analyst", create_analyst_agent("novelty", "small")["agent"])
    # graph.add_node(
    #     "feasibility_analyst", create_analyst_agent("feasibility", "small")["agent"]
    # )
    # graph.add_node("impact_analyst", create_analyst_agent("impact", "small")["agent"])
    # graph.add_node("critique_analyst", create_critique_analyst_agent("small")["agent"])
    # graph.add_node("summary_agent", create_summary_agent("small")["agent"])

    # Add edges
    graph.add_edge(START, "graph_analyst")
    # graph.add_edge("ontologist", "hypothesis_generator")
    # # From initial hypothesis
    # graph.add_edge("hypothesis_generator", "literature_agent")
    # # From refined hypothesis
    # graph.add_edge("hypothesis_refiner", "literature_agent")
    # # # Fork
    # graph.add_edge("literature_agent", "novelty_analyst")
    # graph.add_edge("literature_agent", "feasibility_analyst")
    # graph.add_edge("literature_agent", "impact_analyst")
    # # # Join
    # graph.add_edge("novelty_analyst", "critique_analyst")
    # graph.add_edge("feasibility_analyst", "critique_analyst")
    # graph.add_edge("impact_analyst", "critique_analyst")
    # # graph.add_edge("critique_analyst", END)
    # graph.add_conditional_edges(
    #     "critique_analyst",
    #     improve_hypothesis,
    # )
    graph.add_edge("graph_analyst", END)

    return graph.compile()


hackathon_graph = create_hackathon_graph()
