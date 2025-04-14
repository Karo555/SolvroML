import json
from typing import Any, Dict, Literal, Optional, List
from langchain.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from loguru import logger

# from ..tools.evidence import 
from ..llm.utils import get_model
from ..state import EvidenceAgentPrivateState, HackathonState

EVIDENCE_PROMPT = """
You are a biomedical literature evidence agent.

Your task is to support the following biological relationship with relevant scientific evidence.

Use access to literature databases provided by tools.

Return **exactly 1-3 relevant references** in valid JSON.

Use the following format exactly:

{{
  "relation": "<source> -[:relation]-> <target>",
  "references": [
    {
      "title": "Title of the paper",
      "authors": ["Last, F.", "Smith, A."],
      "year": 2021,
      "source": "PubMed",
      "url": "https://...",
      "snippet": "A short quote from the abstract or result supporting the relation"
    }
  ]
}}

Biological relation:
{source} -[:{relation}]-> {target}

Interpretation:
{interpretation}
"""

# ToolNode with literature tools
evidence_tools = ToolNode([
    ...
])

def create_evidence_agent(
    model: Optional[Literal["large", "small", "reasoning"]] = None,
    **kwargs
) -> Dict[str, Any]:
    llm = get_model(model, **kwargs)

    tool_agent = create_react_agent(
        model=llm,
        tools=evidence_tools,
        prompt=EVIDENCE_PROMPT,
        state_schema=EvidenceAgentPrivateState
    )

    def agent(state: EvidenceAgentPrivateState) -> HackathonState:
        summaries = state.get("mechanistic_summaries", []) or []
        updated_summaries = []

        for summary in summaries:
            relationships = summary.get("relationships", [])
            enriched_relationships = []

            for rel in relationships:
                source = rel.get("source")
                target = rel.get("target")
                relation = rel.get("relation")
                interpretation = rel.get("interpretation", "")

                logger.info(f"📚 Searching for evidence: {source} -[:{relation}]-> {target}")

                prompt = PromptTemplate.from_template(EVIDENCE_PROMPT)
                messages = prompt.invoke({
                    "source": source,
                    "target": target,
                    "relation": relation,
                    "interpretation": interpretation
                }).to_messages()

                try:
                    response = tool_agent.invoke({
                        "messages": messages,
                        "mechanistic_summaries": summaries
                    })

                    raw = response["messages"][-1].content.strip()
                    parsed = json.loads(raw)
                    rel["references"] = parsed.get("references", [])

                except Exception as e:
                    logger.warning(f"❌ Failed to retrieve evidence for {source} → {target}: {e}")
                    rel["references"] = []

                enriched_relationships.append(rel)

            summary["relationships"] = enriched_relationships
            updated_summaries.append(summary)

        return HackathonState(
            mechanistic_summaries=updated_summaries,
            messages=state.get("messages", []),
        )

    return {"agent": agent}