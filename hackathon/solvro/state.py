from typing import Dict, List
from langgraph.graph import MessagesState
from pydantic import BaseModel

class MechanisticSummary(BaseModel):
    path_summary: str
    key_entities: List[Dict[str, str]]
    relationships: List[Dict[str, str]]

class HackathonState(MessagesState):
    subgraph: str
    context: str
    hypothesis: str
    
    

    literature: str
    references: list[str]

    # novelty: str
    # feasibility: str
    # impact: str

    # critique: str
    summary: str
    title: str

    iteration: int
    
    # Graph Analyst agent
    mechanistic_summaries: List[MechanisticSummary] = []