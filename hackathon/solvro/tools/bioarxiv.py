from typing import Optional, Dict, Annotated

import requests
from pydantic import BaseModel
from typing import Optional
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_core.callbacks import CallbackManagerForToolRun
from langgraph.prebuilt.chat_agent_executor import AgentState
from dataclasses import dataclass


BASE_URL = "https://api.biorxiv.org"

class BioRxivAPIManager(BaseModel):
    """
    A manager class for interacting with the BioRxiv API.

    Attributes:
        server (str): The server to use for API requests (default is "biorxiv").
    """
    
    server: str = "biorxiv"

    def validate_server(cls, values):
        """Validate the server attribute."""
        # Add any server validation logic if necessary
        return values

    def fetch_details_by_date_range(
        self, start_date: str, end_date: str, cursor: int = 0,
        category: Optional[str] = None, format: str = "json"
    ):
        """
        Fetches article details within a specified date range.
        """
        url = f"{BASE_URL}/details/{self.server}/{start_date}/{end_date}/{cursor}/{format}"
        if category:
            url += f"?category={category.replace(' ', '_')}"
        return self._get(url)

    def fetch_details_by_doi(self, doi: str, format: str = "json"):
        """
        Fetches article details by DOI.
        """
        url = f"{BASE_URL}/details/{self.server}/{doi}/na/{format}"
        return self._get(url)


    def _get(self, url: str):
        """
        Sends a GET request to the specified URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json() if "json" in url else response.text
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None



class BiorxivQueryRun(BaseTool):  # type: ignore[override]
    """Tool that searches the PubMed API."""

    name: str = "bioarxiv"
    description: str = (
        "BioRxivTool provides access to the bioRxiv preprint repository, enabling search and retrieval of the latest "
        "non-peer-reviewed biomedical research articles. This tool supports querying by keywords, authors, or topics, "
        "and returns metadata such as title, abstract, authors, and publication date. Useful for staying updated on "
        "emerging scientific findings in biology, medicine, and related disciplines."
    )
    api_wrapper: BioRxivAPIManager = Field(default_factory=BioRxivAPIManager)  # type: ignore[arg-type]

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the PubMed tool."""
        return self.api_wrapper.fetch_details_by_date_range(start_date="2025-03-21", end_date="2025-03-28", category=query)
    

# api_wrapper = BioRxivAPIManager(
#                 top_k_results = 3,
#                 ARXIV_MAX_QUERY_LENGTH = 300,
#                 load_max_docs = 3,
#                 load_all_available_meta = False,
#                 doc_content_chars_max = 40000
# )

# @tool("biorxiv", parse_docstring=True)
# def biorxiv(query: str,
#             tool_call_id: str,
#             config: RunnableConfig,
#             state: dict,
#     ) -> str:
#     """
#     Searches and retrieves recent biomedical research articles from the bioRxiv preprint repository.
#     The search is conducted within a fixed date range (2025-03-21 to 2025-03-28) using the given query
#     which may include keywords, topics, or author names. Returns metadata such as title, abstract,
#     authors, and publication date for each matched article.
    
#     Args:
#         query: The keyword, topic, or author to search in the bioRxiv repository.
#         tool_call_id: Unique identifier for the tool call.
#         config: Configuration for the runnable.
#         state: Current state dictionary.
    
#     Returns:
#         str: A string containing metadata of matched bioRxiv articles.
#     """
#     return api_wrapper.fetch_details_by_date_range(
#         start_date="2025-03-21",
#         end_date="2025-03-28",
#         category=query
#     )

@dataclass
class ContextAgentPrivateState(AgentState):
    mechanistic_summaries: Optional[List[Dict[str, Any]]] = None

if __name__ == "__main__":
    from langgraph.prebuilt import ToolNode
    CONTEXT_PROMPT = """
    You are a biomedical entity enrichment assistant.

    Your task is to enrich a given biomedical entity using ontology tools and return structured metadata. 
    Return the result in **valid JSON format only**. Do not include any extra explanation or notes.

    Limit the "definition" to **no more than 300 characters**.

    Use the following format exactly:

    {{
    "definition": "<Concise biological or clinical description, max 300 characters>",
    "ontology_id": "<Ontology or database identifier (e.g., UniProt accession)>",
    "synonyms": ["<synonym1>", "<synonym2>", ...]
    }}

    Entity to enrich:
    {entity}
    """

    import json
    from typing import Any, Dict, Literal, Optional, List

    from langgraph.prebuilt.chat_agent_executor import create_react_agent
    from loguru import logger

    from ..state import ContextAgentPrivateState, HackathonState
    from langchain_openai import ChatOpenAI

    biorxiv_tool = BiorxivQueryRun(api_wrapper=BioRxivAPIManager(
                    top_k_results = 3,
                    ARXIV_MAX_QUERY_LENGTH = 300,
                    load_max_docs = 3,
                    load_all_available_meta = False,
                    doc_content_chars_max = 40000
    ))


    context_tools = ToolNode([
        biorxiv_tool,
    ])


    tool_agent = create_react_agent(
        model=ChatOpenAI(model="gpt-4o-mini"),
        tools=context_tools,
        prompt=CONTEXT_PROMPT,
        state_schema=ContextAgentPrivateState
    )
