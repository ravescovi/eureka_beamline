"""Utility module for converting between YAML and JSON formats.

This module provides functions to convert between YAML and JSON formats,
with proper error handling and type validation.
"""

from typing import Any, Dict, Union
import json
import yaml
from pathlib import Path


def yaml_to_json(yaml_content: Union[str, Path]) -> Dict[str, Any]:
    """Convert YAML content to JSON format.
    
    Args:
        yaml_content: Either a string containing YAML content or a Path object
            pointing to a YAML file.
    
    Returns:
        Dict[str, Any]: The parsed YAML content as a Python dictionary.
    
    Raises:
        yaml.YAMLError: If the YAML content is invalid.
        FileNotFoundError: If yaml_content is a Path and the file doesn't exist.
    """
    if isinstance(yaml_content, Path):
        with open(yaml_content, 'r') as f:
            yaml_content = f.read()
    
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse YAML content: {str(e)}")


def json_to_yaml(json_content: Union[str, Dict[str, Any]], file_path: Union[str, Path, None] = None) -> str:
    """Convert JSON content to YAML format.
    
    Args:
        json_content: Either a string containing JSON content or a Python dictionary.
        file_path: Optional path to save the YAML output. If provided, the YAML
            will be written to this file.
    
    Returns:
        str: The YAML representation of the JSON content.
    
    Raises:
        json.JSONDecodeError: If json_content is a string and contains invalid JSON.
        TypeError: If json_content is neither a string nor a dictionary.
    """
    if isinstance(json_content, str):
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Failed to parse JSON content: {str(e)}", e.doc, e.pos)
    elif isinstance(json_content, dict):
        data = json_content
    else:
        raise TypeError("json_content must be either a string or a dictionary")
    
    yaml_content = yaml.dump(data, default_flow_style=False)
    
    if file_path:
        with open(file_path, 'w') as f:
            f.write(yaml_content)
    
    return yaml_content 