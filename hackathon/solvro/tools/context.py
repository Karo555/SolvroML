from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import InjectedState
from langchain_core.tools import InjectedToolCallId
from typing import Annotated, Dict, Any

from .backends.UniProtAPIWrapper import UniProtAPIWrapper
from .backends.UniProtQueryTool import parse_uniprot_entry

# Initialize UniProt wrapper
api_wrapper = UniProtAPIWrapper()

@tool("query_uniprot", parse_docstring=True)
def query_uniprot(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    state: Annotated[dict, InjectedState],
) -> Dict[str, Any]:
    """
    Searches UniProt for information on a gene or protein. Best used when a node is a gene or biological process involving proteins or enzymes.

    Args:
        query (str): A gene or protein name (e.g., "BRCA1", "IL6").

    Returns:
        dict: A structured dictionary with UniProt metadata (e.g., definition, synonyms, ontology ID, etc.)
    """
    result = api_wrapper.search(query)

    if not result:
        return {
            "error": f"No UniProt entry found for '{query}'.",
            "ontology_id": None,
            "definition": "No entry found.",
            "synonyms": [],
        }

    parsed = parse_uniprot_entry(result)

    return {
        "definition": parsed.get("function") or parsed.get("protein_name") or "No description available.",
        "ontology_id": parsed.get("accession"),
        "synonyms": parsed.get("gene_names", []),
    }
