"""
Unit tests for the Claim model.
"""
import pytest
from datetime import datetime, timedelta
from models.claim import Claim


class TestClaimModel:
    """Test cases for the Claim model."""
    
    def test_create_claim(self, session, sample_policy):
        """Test creating a new claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-NEW789",
            claim_date=datetime.today().date(),
            incident_date=(datetime.today() - timedelta(days=3)).date(),
            description="New test claim",
            claim_amount=3000.00,
            status="Open"
        )
        session.add(claim)
        session.commit()
        
        assert claim.claim_id is not None
        assert claim.policy_id == sample_policy.policy_id
        assert claim.claim_number == "CLM-NEW789"
        assert claim.description == "New test claim"
        assert float(claim.claim_amount) == 3000.00
        assert claim.status == "Open"
    
    def test_claim_repr(self, sample_claim):
        """Test claim string representation."""
        assert repr(sample_claim) == '<Claim CLM-TEST456>'
    
    def test_claim_is_open_true(self, sample_claim):
        """Test is_open method returns True for open claim."""
        assert sample_claim.is_open() is True
    
    def test_claim_is_open_in_progress(self, session, sample_policy):
        """Test is_open method returns True for in progress claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-PROGRESS",
            claim_date=datetime.today().date(),
            incident_date=(datetime.today() - timedelta(days=5)).date(),
            description="In progress claim",
            claim_amount=2000.00,
            status="In Progress"
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_open() is True
    
    def test_claim_is_open_under_review(self, session, sample_policy):
        """Test is_open method returns True for under review claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-REVIEW",
            claim_date=datetime.today().date(),
            incident_date=(datetime.today() - timedelta(days=5)).date(),
            description="Under review claim",
            claim_amount=2000.00,
            status="Under Review"
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_open() is True
    
    def test_claim_is_open_false(self, session, sample_policy):
        """Test is_open method returns False for settled claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-SETTLED",
            claim_date=(datetime.today() - timedelta(days=30)).date(),
            incident_date=(datetime.today() - timedelta(days=35)).date(),
            description="Settled claim",
            claim_amount=4000.00,
            status="Settled",
            resolution_date=datetime.today().date(),
            settlement_amount=4000.00
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_open() is False
    
    def test_claim_is_closed_true(self, session, sample_policy):
        """Test is_closed method returns True for closed claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-CLOSED",
            claim_date=(datetime.today() - timedelta(days=30)).date(),
            incident_date=(datetime.today() - timedelta(days=35)).date(),
            description="Closed claim",
            claim_amount=4000.00,
            status="Closed",
            resolution_date=datetime.today().date()
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_closed() is True
    
    def test_claim_is_closed_denied(self, session, sample_policy):
        """Test is_closed method returns True for denied claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-DENIED",
            claim_date=(datetime.today() - timedelta(days=30)).date(),
            incident_date=(datetime.today() - timedelta(days=35)).date(),
            description="Denied claim",
            claim_amount=4000.00,
            status="Denied",
            resolution_date=datetime.today().date()
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_closed() is True
    
    def test_claim_is_closed_withdrawn(self, session, sample_policy):
        """Test is_closed method returns True for withdrawn claim."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-WITHDRAWN",
            claim_date=(datetime.today() - timedelta(days=30)).date(),
            incident_date=(datetime.today() - timedelta(days=35)).date(),
            description="Withdrawn claim",
            claim_amount=4000.00,
            status="Withdrawn",
            resolution_date=datetime.today().date()
        )
        session.add(claim)
        session.commit()
        
        assert claim.is_closed() is True
    
    def test_claim_is_closed_false(self, sample_claim):
        """Test is_closed method returns False for open claim."""
        assert sample_claim.is_closed() is False
    
    def test_claim_days_since_filed(self, sample_claim):
        """Test days_since_filed calculation."""
        days = sample_claim.days_since_filed()
        expected_days = (datetime.today().date() - sample_claim.claim_date).days
        assert days == expected_days
    
    def test_claim_to_dict(self, sample_claim, sample_policy):
        """Test converting claim to dictionary."""
        claim_dict = sample_claim.to_dict()
        
        assert claim_dict['claim_id'] == sample_claim.claim_id
        assert claim_dict['policy_id'] == sample_policy.policy_id
        assert claim_dict['claim_number'] == "CLM-TEST456"
        assert claim_dict['description'] == "Test incident description"
        assert claim_dict['claim_amount'] == 5000.00
        assert claim_dict['status'] == "Open"
        assert 'claim_date' in claim_dict
        assert 'incident_date' in claim_dict
        assert 'created_at' in claim_dict
        assert 'updated_at' in claim_dict
        assert 'days_since_filed' in claim_dict
        assert claim_dict['is_open'] is True
        assert claim_dict['policy_number'] == "POL-TEST123"
        assert claim_dict['customer_name'] == "Jane Smith"
    
    def test_claim_policy_relationship(self, sample_claim, sample_policy):
        """Test the relationship between claim and policy."""
        assert sample_claim.policy == sample_policy
        assert sample_claim.policy.policy_number == "POL-TEST123"
    
    def test_claim_with_settlement(self, session, sample_policy):
        """Test claim with settlement amount."""
        claim = Claim(
            policy_id=sample_policy.policy_id,
            claim_number="CLM-SETTLEMENT",
            claim_date=(datetime.today() - timedelta(days=30)).date(),
            incident_date=(datetime.today() - timedelta(days=35)).date(),
            description="Claim with settlement",
            claim_amount=10000.00,
            status="Settled",
            resolution_date=datetime.today().date(),
            settlement_amount=9500.00
        )
        session.add(claim)
        session.commit()
        
        assert float(claim.settlement_amount) == 9500.00
        assert claim.resolution_date == datetime.today().date()
