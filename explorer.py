from pathlib import Path
import shutil
from langchain.tools import StructuredTool

from pydantic import BaseModel, Field

AGENT_FOLDER = Path(__file__).parent.resolve()

class ListInput(BaseModel):
    directory: str|Path = Field(..., description="The directory to create or list files from.")

class RemoveFileInput(BaseModel):
    directory: str|Path = Field(..., description="The directory to remove the file from.")
    filename: str = Field(..., description="The filename to remove.")

class GetMetadataInput(BaseModel):
    filename: str|Path = Field(..., description="The filename to get metadata from.")


def create_directory(directory:str|Path) -> str:
    """Create a directory.
    
    Args:
        directory (str): The directory to create.

    Returns:
        str: A message indicating the status of the operation.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    try:
        # Create the directory
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        msg = f"Error creating directory: {e}"
        return msg
    
    return f"Directory created: {directory}"

def list_files_in_directory(directory:str|Path) -> list:
    """List all files in a directory.
    
    Args:
        directory (str): The directory to list files from.

    Returns:
        list: A list of filenames in the directory.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    try:
        # List all files in the directory
        files = [f.name for f in directory.iterdir() if f.is_file()]
    except Exception as e:
        msg = f"Error listing files in directory: {e}"
        return msg
    
    return files

def list_directories_in_directory(directory:str|Path) -> list:
    """List all directories in a directory.
    
    Args:
        directory (str): The directory to list directories from.

    Returns:
        list: A list of directory names in the directory.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    try:
        # List all directories in the directory
        directories = [d.name for d in directory.iterdir() if d.is_dir()]
    except Exception as e:
        msg = f"Error listing directories in directory: {e}"
        return msg
    
    return directories

def list_directory(directory:str|Path) -> list:
    """List all files and directories in a directory.
    
    Args:
        directory (str): The directory to list files and directories from.

    Returns:
        list: A list of filenames and directory names in the directory.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    try:
        # List all files and directories in the directory
        contents = [f.name for f in directory.iterdir()]
    except Exception as e:
        msg = f"Error listing directory: {e}"
        return msg
    
    return contents

def get_file_metadata(filename:str|Path) -> dict:
    """Get metadata of a file.
    
    Args:
        filename (str): The filename to get metadata from.

    Returns:
        dict: A dictionary containing metadata of the file.
    """
    if isinstance(filename, str):
        filename = Path(filename)

    try:
        # Get metadata of the file
        metadata = {
            "name": filename.name,
            "path": str(filename.resolve().parent()),
            "size": filename.stat().st_size,
            "last_modified": filename.stat().st_mtime,
        }
    except Exception as e:
        msg = f"Error getting file metadata: {e}"
        return msg
    
    return metadata

def get_directory_metadata(directory:str|Path) -> dict:
    """Get metadata of a directory.
    
    Args:
        directory (str): The directory to get metadata from.

    Returns:
        dict: A dictionary containing metadata of the directory.
    """

    if isinstance(directory, str):
        directory = Path(directory)

    try:
        # Get metadata of the directory
        metadata = {
            "name": directory.name,
            "path": str(directory.resolve().parent()),
            "files": len(list_files_in_directory(directory)),
            "directories": len(list_directories_in_directory(directory)),
        }
    except Exception as e:
        msg = f"Error getting directory metadata: {e}"
        return msg
    
    return metadata

def remove_file_from_directory(directory:str|Path, filename:str) -> str:
    """Remove a file from a directory.
    
    Args:
        directory (str): The directory to remove the file from.
        filename (str): The filename to remove.

    Returns:
        str: A message indicating the status of the operation.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    filepath = directory / filename

    # Check that the directory absolute path of the file is not in the agent folder
    if filepath.resolve().parent == AGENT_FOLDER:
        return f"Cannot remove files from the agent directory: {filepath.resolve().parent}. Please specify a different directory."

    try:
        # Remove the file from the directory
        filepath.unlink()
    except Exception as e:
        msg = f"Error removing file from directory: {e}"
        return msg
    
    return f"File '{filename}' removed from directory {directory}."

def remove_directory(directory:str|Path) -> str:
    """Remove a directory from a directory.
    
    Args:
        directory (str): The directory to remove the directory from.
        dirname (str): The directory name to remove.

    Returns:
        str: A message indicating the status of the operation.
    """
    if isinstance(directory, str):
        directory = Path(directory)

    if directory.resolve() == AGENT_FOLDER:
        return f"Cannot remove the agent directory: {directory.resolve()}. Please specify a different directory."        
    
    try:
        # If the directory is not empty, remove it recursively
        shutil.rmtree(directory)
    except Exception as e:
        msg = f"Error removing directory from directory: {e}"
        return msg
    
    return f"Directory '{directory.name}' removed from directory {directory.parent}."

tools_explorer = [
    StructuredTool(name="create_directory", func=create_directory, description="Create a directory.",
                   args_schema=ListInput),
    StructuredTool(name="list_files_in_directory", func=list_files_in_directory, description="List all files in a directory.",
                     args_schema=ListInput),
    StructuredTool(name="list_directories_in_directory", func=list_directories_in_directory, description="List all directories in a directory.",
                        args_schema=ListInput),
    StructuredTool(name="list_directory", func=list_directory, description="List all files and directories in a directory.",
                        args_schema=ListInput),
    StructuredTool(name="get_file_metadata", func=get_file_metadata, description="Get metadata of a file.",
                        args_schema=GetMetadataInput),
    StructuredTool(name="get_directory_metadata", func=get_directory_metadata, description="Get metadata of a directory.",
                        args_schema=ListInput),
    StructuredTool(name="remove_file_from_directory", func=remove_file_from_directory, description="Remove a file from a directory.",
                        args_schema=RemoveFileInput),
    StructuredTool(name="remove_directory", func=remove_directory, description="Remove a directory from a directory.",
                        args_schema=ListInput),
]