from pathlib import Path
import json

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class WriterInput(BaseModel):
    filename: str|Path = Field(..., description="The filename to write to.")
    content: str|dict = Field(..., description="The content to write.")

def write_to_file(filename:str|Path, content:str) -> str:
    """Write content to a file.
    
    Args:
        filename (str): The filename to write to.
        content (str): The content to write.

    Returns:
        str: The path of the file written.
    """
    if isinstance(filename, str):
        filename = Path(filename)

    # Make sure the parent directory exists
    filename.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Write content to file
        with filename.open("w") as f:
            f.write(content)
    except Exception as e:
        msg = f"Error writing to file: {e}"
        return msg
    
    msg = f"File written to: {filename}"
    return msg

def write_to_json(filename:str|Path, content:str|dict) -> str:
    """Write content to a JSON file.
    
    Args:
        filename (str): The filename to write to.
        content (dict): The content to write.

    Returns:
        str: The path of the file written.
    """
    if isinstance(filename, str):
        filename = Path(filename)

    if isinstance(content, dict):
        content = json.dumps(content, indent=4, ensure_ascii=False)

    # Make sure the parent directory exists
    filename.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Write content to file
        with filename.open("w") as f:
            f.write(json.dumps(content, indent=4))
    except Exception as e:
        msg = f"Error writing to file: {e}"
        return msg
    
    msg = f"File written to: {filename}"
    return msg

tools_writer = [
    StructuredTool(name="write_to_file", func=write_to_file, 
                    description="Write content to a file.", args_schema=WriterInput,),
    StructuredTool(name="write_to_json", func=write_to_json, 
                    description="Write content to a JSON file.", args_schema=WriterInput),
]