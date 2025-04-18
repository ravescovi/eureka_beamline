"""Base agent class for BITS AI agents.

This module defines the base agent class that all BITS AI agents should inherit from.
It provides common functionality like logging, input validation, and version tracking.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
import logging
import json
from pathlib import Path

class BaseAgent(ABC):
    """Base class for all BITS AI agents.
    
    This class provides common functionality that all agents should have,
    including logging, input validation, and version tracking.
    
    Attributes:
        name (str): The name of the agent
        version (str): The version of the agent
        logger (logging.Logger): Logger instance for the agent
    """
    
    def __init__(self, name: str, version: str = "0.1.0") -> None:
        """Initialize the base agent.
        
        Args:
            name: The name of the agent
            version: The version of the agent
        """
        self.name = name
        self.version = version
        self.logger = logging.getLogger(f"bits.agent.{name}")
        
    @abstractmethod
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for the agent.
        
        Args:
            inputs: Dictionary of input parameters
            
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        pass
        
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality.
        
        Args:
            inputs: Dictionary of input parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing the results
        """
        pass
        
    def log_execution(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Log the execution of the agent.
        
        Args:
            inputs: Dictionary of input parameters
            outputs: Dictionary of output results
        """
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "agent": self.name,
            "version": self.version,
            "inputs": inputs,
            "outputs": outputs
        }
        self.logger.info(json.dumps(log_entry))
        
    def sanitize_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize the output to ensure it's safe to return.
        
        Args:
            output: Dictionary of output results
            
        Returns:
            Dict[str, Any]: Sanitized output dictionary
        """
        # TODO: Implement proper sanitization
        return output 