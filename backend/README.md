# Eureka Beamline Backend

The backend service for the Eureka Beamline project, providing FastAPI endpoints for various beamline agents and tools.

## Features

- IOC Analyzer: Analyze and validate IOC configurations
- Device Generator: Generate device definitions and configurations
- Plan Generator: Create and validate beamline plans
- RESTful API with OpenAPI documentation
- Docker support for easy deployment

## Installation

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/eureka_beamline.git
   cd eureka_beamline/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Docker Setup

```bash
docker-compose up --build
```

## Usage

### Running the Server

```bash
uvicorn eureka_beamline_backend.main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Code Style

This project uses:
- Ruff for linting
- MyPy for type checking
- Black for code formatting

Run the linters:
```bash
ruff check .
mypy .
```

### Testing

Run tests with pytest:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=eureka_beamline_backend
```

## Project Structure

```
backend/
├── eureka_beamline_backend/     # Main package directory
│   ├── agents/                  # Agent implementations
│   ├── routers/                 # FastAPI routers
│   ├── schemas/                 # Pydantic models
│   └── main.py                  # Application entry point
├── tests/                       # Test directory
├── pyproject.toml              # Project configuration
├── Dockerfile                  # Docker configuration
└── README.md                   # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details 