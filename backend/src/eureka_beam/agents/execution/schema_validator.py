"""Schema-Validator Agent for BITS.

This module implements the Schema-Validator Agent that validates configuration
files (devices.yml, etc.) against the BITS schema.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
import jsonschema

from ...agents.base import BaseAgent

class SchemaValidatorAgent(BaseAgent):
    """Agent responsible for validating BITS configuration files.
    
    This agent validates configuration files (devices.yml, etc.) against
    the BITS schema to ensure they meet the required format and contain
    all necessary information.
    
    Attributes:
        name (str): The name of the agent ("bits_schema_validator")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Schema-Validator Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_schema_validator", version)
        self._load_schemas()
        
    def _load_schemas(self) -> None:
        """Load the BITS schema definitions."""
        self.device_schema = {
            "type": "object",
            "required": ["module", "class", "prefix", "kind"],
            "properties": {
                "module": {"type": "string"},
                "class": {"type": "string"},
                "prefix": {"type": "string"},
                "kind": {"type": "string"},
                "read_attrs": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
        
        self.plan_schema = {
            "type": "object",
            "required": ["module", "function"],
            "properties": {
                "module": {"type": "string"},
                "function": {"type": "string"},
                "parameters": {
                    "type": "object",
                    "additionalProperties": {"type": "string"}
                }
            }
        }
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for schema validation.
        
        Args:
            inputs: Dictionary containing:
                - config_files: List of configuration files to validate
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        if "config_files" not in inputs:
            self.logger.error("Missing config_files in inputs")
            return False
            
        return True
        
    def _validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a single configuration file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dict[str, Any]: Validation results for the file
        """
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
                
            if "devices" in file_path:
                schema = self.device_schema
            elif "plans" in file_path:
                schema = self.plan_schema
            else:
                return {
                    "valid": False,
                    "error": f"Unknown configuration type: {file_path}"
                }
                
            jsonschema.validate(instance=config, schema=schema)
            return {"valid": True}
            
        except yaml.YAMLError as e:
            return {
                "valid": False,
                "error": f"YAML parsing error: {str(e)}"
            }
        except jsonschema.exceptions.ValidationError as e:
            return {
                "valid": False,
                "error": f"Schema validation error: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Unexpected error: {str(e)}"
            }
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the schema validation process.
        
        Args:
            inputs: Dictionary containing validation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - results: Validation results for each file
                - summary: Overall validation summary
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        config_files = inputs["config_files"]
        results = {}
        
        for file_path in config_files:
            results[file_path] = self._validate_file(file_path)
            
        valid_count = sum(1 for r in results.values() if r["valid"])
        total_count = len(results)
        
        summary = {
            "total_files": total_count,
            "valid_files": valid_count,
            "invalid_files": total_count - valid_count
        }
        
        result = {
            "results": results,
            "summary": summary
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 