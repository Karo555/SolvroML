from langchain.tools import BaseTool
from typing import Optional
from UniProtAPIWrapper import UniProtAPIWrapper

from langchain.tools import BaseTool
from typing import Optional
from pydantic import Field

class UniProtQueryTool(BaseTool):
    name: str = Field(default="uniprot_query", description="The name of the tool.")
    description: str = Field(default="Searches UniProt for protein or gene information.")
    api_wrapper: UniProtAPIWrapper

    def _run(self, query: str) -> Optional[dict]:
        return self.api_wrapper.search(query)

    async def _arun(self, query: str) -> Optional[dict]:
        raise NotImplementedError("Async not implemented.")

if __name__ == "__main__":
    uniprot_wrapper = UniProtAPIWrapper()
    uniprot_tool = UniProtQueryTool(api_wrapper=uniprot_wrapper)

    test_query = "BRCA1"  # You can replace this with any protein or gene name
    print(f"Querying UniProt for: {test_query}")
    result = uniprot_tool.run(test_query)

    if result:
        print("✅ Result:")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("❌ No results found.")
