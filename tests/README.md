# Naxai SDK Tests

This directory contains tests for the Naxai SDK Python library. The tests are organized by type (unit, integration) and further by resource type.

## Test Structure

```
tests/
├── unit/                      # Unit tests
│   ├── resources/             # Tests for synchronous resources
│   │   ├── voice/             # Voice resource tests
│   │   │   ├── test_voice_resource.py
│   │   │   ├── test_call_resource.py
│   │   │   ├── test_broadcast_resource.py
│   │   │   ├── test_activity_logs_resource.py
│   │   │   └── test_reporting_resource.py
│   │   └── ...
│   ├── resources_async/       # Tests for asynchronous resources
│   │   ├── voice/             # Async voice resource tests
│   │   │   ├── test_voice_resource.py
│   │   │   ├── test_call_resource.py
│   │   │   ├── test_broadcast_resource.py
│   │   │   ├── test_activity_logs_resource.py
│   │   │   └── test_reporting_resource.py
│   │   └── ...
│   └── ...
└── integration/               # Integration tests (to be added)
```

## Prerequisites

Before running the tests, make sure you have the following installed:

1. Python 3.8 or higher
2. pytest
3. pytest-asyncio (for testing async code)

## Installation

To install the required dependencies for testing:

```bash
pip install pytest pytest-asyncio pytest-cov
```

## Running the Tests

### Running All Tests

To run all tests from the project root directory:

```bash
pytest
```

### Running Specific Test Files

To run tests from a specific file:

```bash
pytest tests/unit/resources/voice/test_voice_resource.py
```

### Running Tests for a Specific Resource

To run all tests for a specific resource (e.g., voice):

```bash
pytest tests/unit/resources/voice/
pytest tests/unit/resources_async/voice/
```

### Running Tests with Coverage

To run tests with coverage reporting:

```bash
pytest --cov=naxai
```

For a detailed HTML coverage report:

```bash
pytest --cov=naxai --cov-report=html
```

This will generate a coverage report in the `htmlcov` directory.

### Running Synchronous vs Asynchronous Tests

To run only synchronous tests:

```bash
pytest tests/unit/resources/
```

To run only asynchronous tests:

```bash
pytest tests/unit/resources_async/
```

## Test Configuration

The tests use pytest fixtures to create mock clients and resources. No actual API calls are made during unit testing.

## Adding New Tests

When adding new tests:

1. Follow the existing directory structure
2. Use pytest fixtures for setup
3. Use unittest.mock for mocking API responses
4. Include assertions for both return values and side effects
5. For async tests, use the `@pytest.mark.asyncio` decorator

## Troubleshooting

If you encounter issues with the tests:

1. Ensure all dependencies are installed
2. Check that you're running the tests from the project root directory
3. Verify that the import paths in the test files match your project structure
4. For async tests, ensure you have pytest-asyncio installed