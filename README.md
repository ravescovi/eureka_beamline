# Beamline REPO

This repository houses the configuration files, device definitions, and control scripts used for beamline instrumentation at the APS. It is designed for Bluesky development and the integration of hardware and software components in our experiments.

## Folder Structure

Beamline REPO/
├── Documents/ 
│ ├── IOC_table.yaml 
│ ├── PV_table.yaml 
│ ├── BITS_devices_table.yaml 
│ ├── BITS_test_plans_table.yaml 
│ └── BITS_user_plans_table.yaml 
├── BITS/ 
│ ├── Devices/ 
│ │ └── Device List 
│ ├── Plans/ 
│ │ └── Bluesky Plans ... 
│ └── Test Plans/ 
│ └── Test Plans List ... 
├── IOCs/ 
│ └── ADCameraSim/ 
├── Soft IOCs/ 
│ └── RobotSimPy/ 
└── Scripts/


## Folder Descriptions

### Documents
Contains YAML configuration files that define key aspects of beamline operations:
- **IOC_table.yaml**: Lists all Input/Output Controllers (IOCs) interfacing with beamline hardware.
- **PV_table.yaml**: Defines the process variables (PVs) essential for instrument control and monitoring.
- **BITS_devices_table.yaml**: Provides a detailed table of beamline devices managed under the BITS framework.
- **BITS_test_plans_table.yaml**: Contains configurations and metadata for test plans used to validate Bluesky plan execution.
- **BITS_user_plans_table.yaml**: Stores user-defined plans and custom configurations for personalized experimental workflows.

### BITS
Houses the core Bluesky plans and device definitions:
- **Devices**:  
  - **Device List**: A comprehensive list of all beamline devices available for control.
- **Plans**:  
  - **Bluesky Plans ...**: Scripts that automate standard beamline procedures, including data acquisition and instrument control.
- **Test Plans**:  
  - **Test Plans List ...**: Contains test scripts and sequences for validating and debugging Bluesky plans prior to deployment on hardware.

### IOCs
Includes implementations of hardware controllers:
- **ADCameraSim**: A simulated IOC for the ADCamera, used to test camera control routines and integrate camera data into Bluesky workflows.

### Soft IOCs
Contains software-based (soft) IOCs that simulate hardware behavior:
- **RobotSimPy**: A Python-based soft IOC that simulates a robotic system. This is particularly useful for developing and troubleshooting automated beamline operations in a controlled environment.

### Scripts
This folder is dedicated to additional utility scripts and workflow automation tools to support day-to-day operations, testing, and development tasks.

## Getting Started

1. **Environment Setup**  
   Ensure you have the appropriate Python environment with Bluesky, ophyd, and any other required packages installed.

2. **Configuration**  
   Update the YAML configuration files in the **Documents** folder to reflect your current beamline setup.

3. **Development & Testing**  
   - Use the scripts in the **BITS/Plans** folder for standard beamline operations.
   - Run tests from the **BITS/Test Plans** folder to validate new plan developments.
   - For hardware simulation, refer to the IOCs and Soft IOCs folders.
   - Utilize the **Scripts** folder for additional utility tasks and workflow automation.

4. **Further Documentation**  
   Consult the APS beamline management documentation or contact the Bluesky development team for further instructions and guidelines.

Happy experimenting!