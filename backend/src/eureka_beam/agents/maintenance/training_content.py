"""Training-Content Generator Agent for BITS.

This module implements the Training-Content Generator Agent that generates
training notebooks or tutorials for beamline scientists learning BITS workflows.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from ...agents.base import BaseAgent

class TrainingContentGeneratorAgent(BaseAgent):
    """Agent responsible for generating BITS training content.
    
    This agent generates training notebooks and tutorials for beamline scientists
    learning BITS workflows. It creates interactive content with examples and
    exercises.
    
    Attributes:
        name (str): The name of the agent ("bits_training_content_generator")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Training-Content Generator Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_training_content_generator", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for training content generation.
        
        Args:
            inputs: Dictionary containing:
                - objectives: List of training objectives
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        if "objectives" not in inputs:
            self.logger.error("Missing objectives in inputs")
            return False
            
        return True
        
    def _generate_notebook(self, objective: str) -> str:
        """Generate a Jupyter notebook for a training objective.
        
        Args:
            objective: Training objective to cover
            
        Returns:
            str: Generated notebook content in JSON format
        """
        # TODO: Implement actual notebook generation
        # For now, return a sample notebook
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# BITS Training: {objective}\n",
                        "\n",
                        "This notebook covers the basics of using BITS for beamline operations."
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "from bits import Beamline\n",
                        "\n",
                        "# Initialize the beamline\n",
                        "beamline = Beamline()"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Exercise 1\n",
                        "\n",
                        "Try running a simple scan:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Your code here\n",
                        "beamline.run_experiment('exercise1.yml')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        return json.dumps(notebook, indent=2)
        
    def _generate_tutorial(self, objective: str) -> str:
        """Generate a tutorial document for a training objective.
        
        Args:
            objective: Training objective to cover
            
        Returns:
            str: Generated tutorial content
        """
        return f"""# BITS Tutorial: {objective}

## Overview

This tutorial will guide you through using BITS for {objective}.

## Prerequisites

- Basic Python knowledge
- Understanding of beamline operations
- BITS installed and configured

## Step 1: Setup

1. Start the BITS server:
   ```bash
   bits-server start
   ```

2. Open the web interface:
   ```
   http://localhost:8000
   ```

## Step 2: Basic Operations

1. Initialize the beamline:
   ```python
   from bits import Beamline
   beamline = Beamline()
   ```

2. Configure devices:
   ```python
   beamline.configure_devices("devices.yml")
   ```

## Step 3: Running Experiments

1. Create an experiment file:
   ```yaml
   name: my_experiment
   steps:
     - type: scan
       motor: motor_x
       start: -10
       stop: 10
       points: 100
   ```

2. Run the experiment:
   ```python
   beamline.run_experiment("my_experiment.yml")
   ```

## Exercises

1. Create a scan with multiple motors
2. Add data collection to your scan
3. Save and load experiment configurations

## Next Steps

- Read the API documentation
- Try more complex experiments
- Join the BITS community
"""
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the training content generation process.
        
        Args:
            inputs: Dictionary containing training content parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - notebooks: Generated Jupyter notebooks
                - tutorials: Generated tutorial documents
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        objectives = inputs["objectives"]
        
        notebooks = {
            objective: self._generate_notebook(objective)
            for objective in objectives
        }
        
        tutorials = {
            objective: self._generate_tutorial(objective)
            for objective in objectives
        }
        
        result = {
            "notebooks": notebooks,
            "tutorials": tutorials
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 