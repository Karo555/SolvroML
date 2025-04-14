from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from langgraph.graph import MessagesState
from pydantic import BaseModel
from langgraph.prebuilt.chat_agent_executor import AgentState

class MechanisticSummary(BaseModel):
    path_summary: str
    key_entities: List[Dict[str, str]]
    relationships: List[Dict[str, str]]

@dataclass
class HackathonState(MessagesState):
    subgraph: str
    context: str
    title: str
    statement: str

    literature: str
    references: list[str]

    # novelty: str
    # feasibility: str
    # impact: str

    critique: str
    summary: str
    title: str

    iteration: int
    
    # Graph Analyst output
    mechanistic_summaries: Optional[List[Dict[str, Any]]] = None
    
@dataclass
class ContextAgentPrivateState(AgentState):
    mechanistic_summaries: Optional[List[Dict[str, Any]]] = None
    
@dataclass
class EvidenceAgentPrivateState(AgentState):
    mechanistic_summaries: Optional[List[Dict[str, Any]]] = None