from typing import Optional, Dict

import requests
from pydantic import BaseModel
from typing import Optional
from langchain_core.tools import BaseTool
from pydantic import Field
from langchain_core.callbacks import CallbackManagerForToolRun

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
