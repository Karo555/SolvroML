import json
from typing import Any, Dict, Literal, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.messages import AIMessage
from loguru import logger

from ..state import HackathonState
from ..llm.utils import get_model


class HypothesisOutput(BaseModel):
    title: str
    statement: str


HYPOTHESIS_PROMPT = """
You are a biomedical research assistant tasked with synthesizing a compelling research hypothesis based on the provided data.

You have:
- Mechanistic summaries derived from a biomedical knowledge graph.
- Background knowledge for each biological entity.
- Literature references supporting each relationship.

Your task:
- Analyze the pathways and their logic.
- Combine them into a coherent hypothesis.
- Output a **concise and informative hypothesis** that a biomedical researcher might want to test.

Return only valid JSON in the following format:

{{
  "title": "<Concise hypothesis title>",
  "statement": "<Biologically sound research hypothesis based on the observed mechanisms>"
}}

Mechanistic Summaries:
{mechanistic_summaries}
"""


def create_hypothesis_synthesis_agent(
    model: Optional[Literal["large", "small", "reasoning"]] = None,
    **kwargs
) -> Dict[str, Any]:
    """Creates a Hypothesis Synthesis Agent."""

    llm = get_model(model, **kwargs).with_structured_output(HypothesisOutput)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a biomedical hypothesis generation assistant."),
        ("human", HYPOTHESIS_PROMPT)
    ])

    chain = prompt | llm

    def agent(state: HackathonState) -> HackathonState:
        logger.info("🧠 Synthesizing hypothesis from graph and context")

        try:
            summaries = json.dumps(state.get("mechanistic_summaries", []), indent=2)
            result: HypothesisOutput = chain.invoke({
                "mechanistic_summaries": summaries
            })

            logger.info(f"✅ Hypothesis synthesized: {result.title}")
            return HackathonState(
                title=result.title,
                statement=result.statement,
                mechanistic_summaries=state.get("mechanistic_summaries", []),
                messages=state.get("messages", []) + [
                    AIMessage(name="hypothesis_agent", content=f"Title: {result.title}\nStatement: {result.statement}")
                ],
            )

        except Exception as e:
            logger.warning(f"❌ Failed to synthesize hypothesis: {e}")
            return HackathonState(
                title="[Failed to generate title]",
                statement="[Failed to generate statement]",
                mechanistic_summaries=state.get("mechanistic_summaries", []),
                messages=state.get("messages", []) + [
                    AIMessage(name="hypothesis_agent", content="Failed to generate hypothesis.")
                ],
            )

    return {"agent": agent}
