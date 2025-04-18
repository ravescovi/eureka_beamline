"""Package Creation Agent for BITS.

This module implements the Package Creation Agent that scaffolds new BITS packages
or ingests existing ones, emitting a sequenced task list for downstream agents.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml

from ...agents.base import BaseAgent

class PackageCreationAgent(BaseAgent):
    """Agent responsible for creating or ingesting BITS packages.
    
    This agent handles the initial setup of a BITS package, either by creating
    a new one from scratch or by ingesting an existing package. It generates
    a sequenced task list for downstream agents to process.
    
    Attributes:
        name (str): The name of the agent ("bits_package_creator")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Package Creation Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_package_creator", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for package creation.
        
        Args:
            inputs: Dictionary containing:
                - package_state: Either "empty" or "existing"
                - package_path: URL or path to the package
                - description: Name and description of the beamline
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        required_fields = ["package_state", "package_path", "description"]
        if not all(field in inputs for field in required_fields):
            self.logger.error("Missing required fields in inputs")
            return False
            
        if inputs["package_state"] not in ["empty", "existing"]:
            self.logger.error("Invalid package_state value")
            return False
            
        return True
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the package creation process.
        
        Args:
            inputs: Dictionary containing package creation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - tasks: List of tasks for downstream agents
                - package_info: Information about the created/ingested package
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        tasks = [
            {
                "action": "request_ioc_links",
                "description": "Prompt for IOC definitions"
            },
            {
                "action": "ioc_analyzer",
                "inputs": {
                    "ioc_text": "<IOC definitions>"
                }
            },
            {
                "action": "bits_device_generator",
                "inputs": {
                    "bits_config": "<analyzer output>"
                }
            },
            {
                "action": "bits_plan_generator",
                "inputs": {
                    "instructions": "<experiment spec>"
                }
            }
        ]
        
        package_info = {
            "state": inputs["package_state"],
            "path": str(inputs["package_path"]),
            "description": inputs["description"]
        }
        
        result = {
            "tasks": tasks,
            "package_info": package_info
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 