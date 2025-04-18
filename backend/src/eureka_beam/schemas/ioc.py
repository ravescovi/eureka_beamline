"""Schema definitions for IOC analyzer.

This module contains Pydantic models for IOC analyzer input and output.
"""

from typing import Dict, Any
from pydantic import BaseModel

class IOCAnalyzerInput(BaseModel):
    """Input model for IOC analyzer endpoint.
    
    Attributes:
        ioc_name: Name of the IOC to analyze.
        config_file: Path to the IOC configuration file.
        options: Optional analysis configuration.
    """
    ioc_name: str
    config_file: str
    options: Dict[str, Any] = {}

class IOCAnalyzerOutput(BaseModel):
    """Output model for IOC analyzer endpoint.
    
    Attributes:
        status: Analysis status (success/failure).
        message: Description of the analysis result.
        details: Additional analysis details.
    """
    status: str
    message: str
    details: Dict[str, Any] 