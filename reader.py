from pathlib import Path
import json

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class ReaderInput(BaseModel):
    filename: str|Path = Field(..., description="The filename to read from.")

def read_from_file(filename:str|Path) -> str:
    """Read content from a file.
    
    Args:
        filename (str): The filename to read from.

    Returns:
        str: The content read from the file.
    """
    if isinstance(filename, str):
        filename = Path(filename)

    try:
        # Read content from file
        with filename.open("r") as f:
            content = f.read()
    except Exception as e:
        msg = f"Error reading from file: {e}"
        return msg
    
    return content

def read_from_json(filename:str|Path) -> dict:
    """Read content from a JSON file.
    
    Args:
        filename (str): The filename to read from.

    Returns:
        dict: The content read from the file.
    """
    if isinstance(filename, str):
        filename = Path(filename)

    try:
        # Read content from file
        with filename.open("r") as f:
            content = json.load(f)
    except Exception as e:
        msg = f"Error reading from file: {e}"
        return msg
    
    return content

tools_reader = [
    StructuredTool(name="read_from_file", func=read_from_file, description="Read content from a file.",
                   args_schema=ReaderInput),
    StructuredTool(name="read_from_json", func=read_from_json, description="Read content from a JSON file.",
                   args_schema=ReaderInput),
]