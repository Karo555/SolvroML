import os
from langchain.agents import Tool
from ard.apimanagers.pubmed import PubmedQueryRun, PubMedAPIWrapperImproved
from ard.apimanagers.arxiv import ArxivAPIWrapper
from ard.apimanagers.bioportal import BioPortalClient, BioPortalQueryRun
from ard.apimanagers.mesh import MeSHAPIWrapper
from ard.apimanagers.bioarxiv import BioRxivAPIManager, BiorxivQueryRun


arxiv_api = ArxivAPIWrapper(top_k_results=3,
                            ARXIV_MAX_QUERY_LENGTH=300,
                            load_max_docs=3,
                            load_all_available_meta=False,
                            doc_content_chars_max=40000)


pubmed_tool = PubmedQueryRun(
    api_wrapper=PubMedAPIWrapperImproved(api_key=os.getenv("PUBMED_API_KEY"))
)


bioportal_tool = BioPortalQueryRun(
    api_wrapper=BioPortalClient(api_key=os.getenv("BIOPORTAL_API_KEY"))
)

biorxiv_tool = BiorxivQueryRun(api_wrapper=BioRxivAPIManager())

mesh_api = MeSHAPIWrapper()
