from langchain.tools import BaseTool
from pydantic import Field, SkipValidation
from SolvroML.hackathon.solvro.tools.DisGeNETAPIWrapper import DisGeNETAPIWrapper
from typing import List, Optional
import dotenv
import json

dotenv.load_dotenv()

# === LangChain Tool ===
class DisGeNETQueryTool(BaseTool):
    name: str = Field(default="disgenet_query", description="Searches DisGeNET for gene-disease associations by NCBI gene ID.")
    description: str = Field(default="Returns disease associations for a given NCBI gene ID using DisGeNET.")
    api_wrapper: SkipValidation[DisGeNETAPIWrapper]

    def _run(self, query: str) -> Optional[dict]:
        return self.api_wrapper.search_by_gene_ncbi_id(query)

    async def _arun(self, query: str) -> Optional[dict]:
        raise NotImplementedError("Async not supported.")
    
def format_disgenet_results(payload: list) -> str:
    lines = []
    for r in payload:
        name = r.get("diseaseName", "Unknown")
        cui = r.get("diseaseUMLSCUI", "N/A")
        score = r.get("score", "N/A")
        lines.append(f"- **{name}** (CUI: `{cui}`, Score: `{score}`)")
    return "\n".join(lines)


# === Test Run ===
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    disgenet_token = os.getenv("DISGENET_API_KEY")
    wrapper = DisGeNETAPIWrapper(api_key=disgenet_token)
    tool = DisGeNETQueryTool(api_wrapper=wrapper)

    gene_ncbi_id = "5781"  # Example: PTPN22 (RA-relevant gene)
    print(f"🔍 Querying DisGeNET for NCBI gene ID: {gene_ncbi_id}")
    results = tool.run(gene_ncbi_id)

    if results:
        payload = results.get("payload", [])
        print(f"\n✅ Retrieved {len(payload)} disease associations.\n")
        print("🔎 First raw payload item:")
        print(json.dumps(payload[0], indent=2))  # Inspect the structure
        for r in payload[:5]:
            disease_name = r.get("diseaseName", "Unknown")
            disease_id = r.get("diseaseUMLSCUI", "N/A")
            score = r.get("score", "N/A")
            print(f"- Disease: {disease_name} | Score: {score} | ID: {disease_id}")
        else:
            print("❌ No results or an error occurred.")
    print("\n🔍 Formatted results:")
    print(format_disgenet_results(payload[:10]))

