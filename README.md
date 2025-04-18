# Eureka Beamline

A comprehensive toolkit for beamline control and automation, featuring both a VS Code extension and FastAPI backend services.

## Project Structure

```
/eureka_beamline/                ← Root monorepo
├── shared/                      ← Shared schemas and utilities
├── backend/                     ← FastAPI agent service
├── recipes/                     ← Deployment recipes and example workflows
├── scripts/                     ← Utility scripts for automation and setup
├── docker-compose.yml           ← Dev orchestration (backend + soft-IOCs)
└── README.md                    ← This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code with [BitsCode Extension](https://github.com/ravescovi/bitscode)
- Python 3.11+
- Node.js 16+

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/eureka_beamline.git
   cd eureka_beamline
   ```

2. Start the backend and soft-IOCs:
   ```bash
   docker-compose up --build
   ```

3. Install the BitsCode VS Code extension:
   - Visit [BitsCode Extension Repository](https://github.com/ravescovi/bitscode)
   - Follow the installation instructions in the repository

## Backend Service

The backend service is built with FastAPI and provides RESTful endpoints for various beamline agents:

- IOC Analyzer
- Device Generator
- Plan Generator

### API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## VS Code Extension

The BitsCode VS Code extension provides an integrated development experience for beamline control. The extension is maintained in a separate repository:

- [BitsCode Extension Repository](https://github.com/ravescovi/bitscode)
- Command Palette integration
- Context menu actions
- Task list visualization
- Agent logs and error messages

## Adding New Agents

1. Define the agent schema in `shared/agent-schemas/`
2. Implement the backend router in `backend/routers/`
3. Create the VS Code command in the [BitsCode Extension Repository](https://github.com/ravescovi/bitscode)
4. Add tests in respective test directories

## Development Guidelines

- Use type hints and docstrings for all Python code
- Follow PEP 257 for docstring conventions
- Write tests using pytest
- Use Ruff for linting
- Keep the shared schemas in sync between frontend and backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

[Your License Here]

## Contact

[Your Contact Information]