import re

SUBGRAPH_FILE_EXTENSION = ".subgraph.json"


def sanitize_filename(file_name: str) -> str:
    """Normalize file name by replacing all non-alphanumeric characters with underscores."""
    # Replace all non-alphanumeric characters with underscores
    normalized = re.sub(r"[^a-zA-Z0-9]", "_", file_name)
    # Reduce multiple underscores to a single underscore
    normalized = re.sub(r"_+", "_", normalized)
    return normalized


def get_subgraph_file_name(subgraph_name: str) -> str:
    return f"{subgraph_name}{SUBGRAPH_FILE_EXTENSION}"


def get_subgraph_name(subgraph_path: str) -> str:
    subgraph_filename = subgraph_path.split("/")[-1]
    return subgraph_filename.split(SUBGRAPH_FILE_EXTENSION)[0]
