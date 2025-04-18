"""BITS Plan Generator Agent.

This module implements the BITS Plan Generator Agent that transforms experiment
instructions or existing plans into BITS-compliant Bluesky plan functions.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

from ...agents.base import BaseAgent

class PlanGeneratorAgent(BaseAgent):
    """Agent responsible for generating BITS plan functions.
    
    This agent transforms experiment instructions or existing plans into
    BITS-compliant Bluesky plan functions. It ensures all generated plans
    follow BITS standards and best practices.
    
    Attributes:
        name (str): The name of the agent ("bits_plan_generator")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Plan Generator Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_plan_generator", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for plan generation.
        
        Args:
            inputs: Dictionary containing:
                - instructions: Experiment instructions or plan specification
                - existing_plan_code: Optional existing plan code
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        if "instructions" not in inputs:
            self.logger.error("Missing instructions in inputs")
            return False
            
        return True
        
    def _parse_instructions(self, instructions: str) -> Dict[str, Any]:
        """Parse experiment instructions into structured format.
        
        Args:
            instructions: Raw experiment instructions
            
        Returns:
            Dict[str, Any]: Parsed instruction parameters
        """
        # TODO: Implement more sophisticated instruction parsing
        # For now, return a sample parsed structure
        return {
            "scan_type": "line_scan",
            "span": 20,
            "step": 0.2,
            "dwell": 0.05,
            "detectors": ["XRF", "ptycho"]
        }
        
    def _generate_plan_code(self, params: Dict[str, Any]) -> str:
        """Generate Bluesky plan code from parsed parameters.
        
        Args:
            params: Parsed instruction parameters
            
        Returns:
            str: Generated plan code
        """
        plan_code = f"""from bluesky.plan_stubs import scan

def line_scan(detector, motor, span={params['span']}, step={params['step']}, dwell={params['dwell']}):
    \"\"\"±{{span}} µm scan, XRF & ptycho enabled\"\"\"
    x0 = motor.position.read() - span
    x1 = motor.position.read() + span
    yield from scan([detector], motor, x0, x1, int(2*span/step))
"""
        return plan_code
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plan generation process.
        
        Args:
            inputs: Dictionary containing plan generation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - plan_code: Generated Bluesky plan code
                - parsed_params: Parsed instruction parameters
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        instructions = inputs["instructions"]
        existing_code = inputs.get("existing_plan_code", "")
        
        parsed_params = self._parse_instructions(instructions)
        plan_code = self._generate_plan_code(parsed_params)
        
        result = {
            "plan_code": plan_code,
            "parsed_params": parsed_params
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 