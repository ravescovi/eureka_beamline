"""Test-Plan & Simulation Agent for BITS.

This module implements the Test-Plan & Simulation Agent that auto-generates
unit tests and simulation scripts to validate devices and plans in CI.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

from ...agents.base import BaseAgent

class TestPlanSimulationAgent(BaseAgent):
    """Agent responsible for generating test plans and simulations.
    
    This agent auto-generates unit tests and simulation scripts to validate
    devices and plans in CI. It ensures comprehensive test coverage and
    proper simulation setup.
    
    Attributes:
        name (str): The name of the agent ("bits_test_plan_simulation")
        version (str): The version of the agent
    """
    
    def __init__(self, version: str = "0.1.0") -> None:
        """Initialize the Test-Plan & Simulation Agent.
        
        Args:
            version: The version of the agent
        """
        super().__init__("bits_test_plan_simulation", version)
        
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate the inputs for test plan generation.
        
        Args:
            inputs: Dictionary containing:
                - devices: List of device modules from devices.yml
                - plans: List of plan modules to test
                
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        required_fields = ["devices", "plans"]
        if not all(field in inputs for field in required_fields):
            self.logger.error("Missing required fields in inputs")
            return False
            
        return True
        
    def _generate_device_tests(self, device: str) -> str:
        """Generate unit tests for a device.
        
        Args:
            device: Device module name
            
        Returns:
            str: Generated test code
        """
        return f"""import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

from apsbits.devices.{device} import {device.title()}Device

def test_{device}_positions():
    \"\"\"Test device position reading and setting.\"\"\"
    device = {device.title()}Device()
    assert device.position.read() is not None

def test_{device}_movement():
    \"\"\"Test device movement commands.\"\"\"
    device = {device.title()}Device()
    device.move(10.0)
    assert abs(device.position.read() - 10.0) < 0.1
"""
        
    def _generate_plan_tests(self, plan: str) -> str:
        """Generate unit tests for a plan.
        
        Args:
            plan: Plan module name
            
        Returns:
            str: Generated test code
        """
        return f"""import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

from apsbits.plans.{plan} import line_scan

def test_line_scan():
    \"\"\"Test line scan plan execution.\"\"\"
    from ophyd.sim import motor1, det1
    plan = line_scan(det1, motor1)
    assert plan is not None
"""
        
    def _generate_simulation_script(self, devices: List[str], plans: List[str]) -> str:
        """Generate simulation script for testing.
        
        Args:
            devices: List of device modules
            plans: List of plan modules
            
        Returns:
            str: Generated simulation script
        """
        script = """#!/usr/bin/env python
from ophyd.sim import motor1, det1
from bluesky import RunEngine

# Create simulated devices
devices = {
    'motor': motor1,
    'detector': det1
}

# Create RunEngine
RE = RunEngine({})

# Import and test plans
"""
        
        for plan in plans:
            script += f"from apsbits.plans.{plan} import line_scan\n"
            
        script += """
# Run test scans
for plan in [line_scan]:
    RE(plan(devices['detector'], devices['motor']))
"""
        
        return script
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the test plan generation process.
        
        Args:
            inputs: Dictionary containing test generation parameters
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - device_tests: Generated device test files
                - plan_tests: Generated plan test files
                - simulation_script: Generated simulation script
        """
        if not self.validate_inputs(inputs):
            raise ValueError("Invalid inputs provided")
            
        devices = inputs["devices"]
        plans = inputs["plans"]
        
        device_tests = {
            f"test_{device}.py": self._generate_device_tests(device)
            for device in devices
        }
        
        plan_tests = {
            f"test_{plan}.py": self._generate_plan_tests(plan)
            for plan in plans
        }
        
        simulation_script = self._generate_simulation_script(devices, plans)
        
        result = {
            "device_tests": device_tests,
            "plan_tests": plan_tests,
            "simulation_script": simulation_script
        }
        
        self.log_execution(inputs, result)
        return self.sanitize_output(result) 