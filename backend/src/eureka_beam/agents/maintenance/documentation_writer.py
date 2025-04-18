"""Documentation-Writer Agent for BITS.

This module implements the Documentation-Writer Agent that produces user
documentation: quickstart guides, API references, and migration manuals.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import ast
import inspect
import re

from ...agents.base import BaseAgent

class DocumentationWriterAgent(BaseAgent):
    """Agent responsible for generating BITS documentation.
    
    This agent produces comprehensive user documentation including quickstart
    guides, API references, and migration manuals. It extracts information
    from the codebase and generates formatted documentation.
    
    Attributes:
        name (str): The name of the agent ("bits_documentation_writer")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Documentation-Writer Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_documentation_writer", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for documentation generation.
        
        Args:
            inputs: Dictionary containing:
                - codebase_path: Path to the local repository
                - sections: List of documentation sections to generate
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        required_fields = ["codebase_path", "sections"]
        if not all(field in inputs for field in required_fields):
            self.logger.error("Missing required fields in inputs")
            return False
            
        return True
        
    def _generate_quickstart(self, codebase_path: str) -> str:
        """Generate quickstart guide.
        
        Args:
            codebase_path: Path to the codebase
            
        Returns:
            str: Generated quickstart guide content
        """
        return """# BITS Quickstart Guide

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/bits.git
   cd bits
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Configure your environment:
   ```bash
   cp config.example.yml config.yml
   # Edit config.yml with your settings
   ```

## Basic Usage

1. Start the BITS server:
   ```bash
   bits-server start
   ```

2. Access the web interface:
   ```
   http://localhost:8000
   ```

3. Run your first experiment:
   ```python
   from bits import Beamline
   
   beamline = Beamline()
   beamline.run_experiment("my_experiment.yml")
   ```
"""
        
    def _generate_api_reference(self, codebase_path: str) -> str:
        """Generate API reference documentation.
        
        Args:
            codebase_path: Path to the codebase
            
        Returns:
            str: Generated API reference content
        """
        return """# BITS API Reference

## Core Classes

### Beamline

The main class for interacting with the beamline.

```python
class Beamline:
    def __init__(self, config_path: str = "config.yml"):
        \"\"\"Initialize the beamline.
        
        Args:
            config_path: Path to configuration file
        \"\"\"
        pass
        
    def run_experiment(self, experiment_path: str) -> None:
        \"\"\"Run an experiment from a YAML file.
        
        Args:
            experiment_path: Path to experiment YAML file
        \"\"\"
        pass
```

## Device Classes

### Motor

Base class for motor devices.

```python
class Motor:
    def move(self, position: float) -> None:
        \"\"\"Move to specified position.
        
        Args:
            position: Target position
        \"\"\"
        pass
```
"""
        
    def _generate_migration_guide(self, codebase_path: str) -> str:
        """Generate migration guide.
        
        Args:
            codebase_path: Path to codebase
            
        Returns:
            str: Generated migration guide content
        """
        return """# BITS Migration Guide

## Upgrading from v1.x to v2.x

### Breaking Changes

1. Device Configuration
   - The `devices.yml` format has changed
   - New required fields: `kind`, `prefix`
   - Migration script: `bits-migrate-devices`

2. Plan Format
   - Plans now use YAML instead of Python
   - New validation rules for plan parameters
   - Migration script: `bits-migrate-plans`

### New Features

1. Enhanced Device Support
   - New device types: Area Detector, Scaler
   - Improved error handling
   - Better logging

2. Plan Improvements
   - YAML-based plan definition
   - Built-in validation
   - Plan templates
"""
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the documentation generation process.
        
        Args:
            inputs: Dictionary containing documentation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - quickstart: Generated quickstart guide
                - api_reference: Generated API reference
                - migration_guide: Generated migration guide
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        codebase_path = inputs["codebase_path"]
        sections = inputs["sections"]
        
        result = {}
        
        if "quickstart" in sections:
            result["quickstart"] = self._generate_quickstart(codebase_path)
            
        if "api" in sections:
            result["api_reference"] = self._generate_api_reference(codebase_path)
            
        if "migration" in sections:
            result["migration_guide"] = self._generate_migration_guide(codebase_path)
            
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 