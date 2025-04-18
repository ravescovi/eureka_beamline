"""BITS Device Generator Agent.

This module implements the BITS Device Generator Agent that generates Python device
classes and validated YAML from IOC analysis or stubs.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml

from ...agents.base import BaseAgent

class DeviceGeneratorAgent(BaseAgent):
    """Agent responsible for generating BITS device classes.
    
    This agent generates Python device classes and validated YAML configuration
    from IOC analysis output or existing device stubs. It ensures all generated
    code follows BITS standards and best practices.
    
    Attributes:
        name (str): The name of the agent ("bits_device_generator")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Device Generator Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_device_generator", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for device generation.
        
        Args:
            inputs: Dictionary containing:
                - bits_config: YAML output from IOC Analyzer
                - existing_device_code: Optional Python stub
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        if "bits_config" not in inputs:
            self.logger.error("Missing bits_config in inputs")
            return False
            
        return True
        
    def _generate_device_class(self, device_config: Dict[str, Any]) -> str:
        """Generate a Python device class from configuration.
        
        Args:
            device_config: Device configuration dictionary
            
        Returns:
            str: Generated Python device class code
        """
        device_name = list(device_config.keys())[0]
        config = device_config[device_name]
        
        class_code = f"""from apsbits.devices import MotorBase
from ophyd import Signal, Component as Cpt

class {device_name.title()}Device(MotorBase):
    \"\"\"Generated for prefix '{config['prefix']}'\"
    
    position = Cpt(Signal, 'POS', dtype=float, units='mm')
"""
        return class_code
        
    def _generate_yaml_config(self, device_config: Dict[str, Any]) -> str:
        """Generate YAML configuration for the device.
        
        Args:
            device_config: Device configuration dictionary
            
        Returns:
            str: Generated YAML configuration
        """
        device_name = list(device_config.keys())[0]
        config = device_config[device_name]
        
        yaml_config = {
            device_name: {
                "module": f"apsbits.devices.{device_name}",
                "class": f"{device_name.title()}Device",
                "prefix": config["prefix"],
                "read_attrs": config["read_attrs"]
            }
        }
        
        return yaml.dump(yaml_config)
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the device generation process.
        
        Args:
            inputs: Dictionary containing device generation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - device_class: Generated Python device class code
                - yaml_config: Generated YAML configuration
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        bits_config = inputs["bits_config"]
        existing_code = inputs.get("existing_device_code", "")
        
        device_class = self._generate_device_class(bits_config)
        yaml_config = self._generate_yaml_config(bits_config)
        
        result = {
            "device_class": device_class,
            "yaml_config": yaml_config
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 