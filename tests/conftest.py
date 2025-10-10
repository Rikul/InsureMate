"""
Test configuration and fixtures for InsureMate test suite.
"""
import pytest
from app import app as flask_app
from models.database import db as _db
from models.agency import Agency
from models.agent import Agent
from models.customer import Customer
from models.policy import Policy
from models.claim import Claim
from datetime import datetime, timedelta


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    ctx = flask_app.app_context()
    ctx.push()
    
    yield flask_app
    
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """Create database for the tests."""
    _db.create_all()
    
    yield _db
    
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db, app):
    """Create a new database session for a test."""
    # Clear all data from the database before each test
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    
    yield db.session
    
    # Rollback any uncommitted changes
    db.session.rollback()
    db.session.remove()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_agency(session):
    """Create a sample agency for testing."""
    agency = Agency(
        name="Test Insurance Agency",
        address="123 Main St",
        city="Test City",
        state="TS",
        zip_code="12345",
        phone="555-1234",
        website="https://testinsurance.com"
    )
    session.add(agency)
    session.commit()
    return agency


@pytest.fixture
def sample_agent(session, sample_agency):
    """Create a sample agent for testing."""
    agent = Agent(
        agency_id=sample_agency.agency_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@testinsurance.com",
        phone="555-5678"
    )
    session.add(agent)
    session.commit()
    return agent


@pytest.fixture
def sample_customer(session):
    """Create a sample customer for testing."""
    customer = Customer(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=datetime(1990, 1, 1).date(),
        email="jane.smith@example.com",
        phone="555-9012",
        address="456 Oak Ave",
        city="Test Town",
        state="TS",
        zip_code="54321"
    )
    session.add(customer)
    session.commit()
    return customer


@pytest.fixture
def sample_policy(session, sample_agent, sample_customer):
    """Create a sample policy for testing."""
    policy = Policy(
        agent_id=sample_agent.agent_id,
        customer_id=sample_customer.customer_id,
        policy_number="POL-TEST123",
        policy_type="Auto Insurance",
        coverage_amount=100000.00,
        premium=1200.00,
        start_date=datetime.today().date(),
        end_date=(datetime.today() + timedelta(days=365)).date(),
        policy_status="Active"
    )
    session.add(policy)
    session.commit()
    return policy


@pytest.fixture
def sample_claim(session, sample_policy):
    """Create a sample claim for testing."""
    claim = Claim(
        policy_id=sample_policy.policy_id,
        claim_number="CLM-TEST456",
        claim_date=datetime.today().date(),
        incident_date=(datetime.today() - timedelta(days=7)).date(),
        description="Test incident description",
        claim_amount=5000.00,
        status="Open"
    )
    session.add(claim)
    session.commit()
    return claim
