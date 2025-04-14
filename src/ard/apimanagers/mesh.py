import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class MeSHAPIWrapper(BaseModel):
    """
    Wrapper around the MeSH RDF API.

    This wrapper uses the MeSH RDF API to search for descriptors and fetch their details.

    Parameters:
        base_url: Base URL for the MeSH RDF API.
        max_results: Maximum number of search results to return.
    """

    base_url: str = "https://id.nlm.nih.gov/mesh/"
    max_results: int = 10

    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the environment is set up correctly."""
        return values

    def search_descriptors(self, term: str) -> List[Dict[str, Any]]:
        """
        Search for MeSH descriptors matching the given term.

        Args:
            term: The search term.

        Returns:
            A list of dictionaries containing descriptor information.
        """
        encoded_term = urllib.parse.quote(term)
        url = f"{self.base_url}lookup/descriptor?label={encoded_term}&match=contains&limit={self.max_results}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []

    def get_descriptor_details(self, descriptor_ui: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve details for a specific MeSH descriptor using its unique identifier.

        Args:
            descriptor_ui: The unique identifier (e.g., 'D003920') of the descriptor.

        Returns:
            A dictionary containing descriptor details, or None if an error occurs.
        """
        url = f"{self.base_url}descriptor/{descriptor_ui}.json"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data
        except Exception as e:
            logger.error(f"Error retrieving descriptor details: {e}")
            return None
    