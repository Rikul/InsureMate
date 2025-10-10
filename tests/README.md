# Test Suite Documentation

This directory contains the test suite for the InsureMate application.

## Test Structure

### Unit Tests (Models)
- `test_agency_model.py` - Tests for the Agency model
- `test_agent_model.py` - Tests for the Agent model
- `test_customer_model.py` - Tests for the Customer model
- `test_policy_model.py` - Tests for the Policy model
- `test_claim_model.py` - Tests for the Claim model

### Integration Tests (Routes)
- `test_agency_routes.py` - Tests for agency API and web routes
- `test_claim_routes.py` - Tests for claim API and web routes

### Application Tests
- `test_app.py` - Tests for main application functionality, error handlers, and context processors

## Test Fixtures

The `conftest.py` file contains shared test fixtures:
- `app` - Flask application configured for testing
- `db` - Database instance
- `session` - Database session for each test
- `client` - Test client for making HTTP requests
- `sample_agency` - Fixture that creates a sample agency
- `sample_agent` - Fixture that creates a sample agent
- `sample_customer` - Fixture that creates a sample customer
- `sample_policy` - Fixture that creates a sample policy
- `sample_claim` - Fixture that creates a sample claim

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_agency_model.py
```

### Run specific test class
```bash
pytest tests/test_agency_model.py::TestAgencyModel
```

### Run specific test method
```bash
pytest tests/test_agency_model.py::TestAgencyModel::test_create_agency
```

### Run with coverage
```bash
pytest --cov=models --cov=routes --cov=app --cov-report=term-missing
```

### Run with verbose output
```bash
pytest -v
```

## Test Coverage

Current coverage (as of latest run):
- **Overall**: 61%
- **Models**: 100% (fully tested)
- **Routes**: ~60% (core routes well-covered)
- **App**: 93%

## Writing New Tests

When adding new tests:
1. Follow the existing naming convention: `test_<functionality>.py`
2. Use descriptive test method names: `test_<what_is_being_tested>`
3. Use the fixtures in `conftest.py` for consistent test data
4. Add docstrings to test classes and methods
5. Keep tests isolated - each test should be independent
6. Clean up after tests (fixtures handle this automatically)

## Test Database

Tests use an in-memory SQLite database that is created fresh for each test session. This ensures:
- Fast test execution
- No interference between tests
- No need to clean up test data manually
- Tests don't affect the development database
