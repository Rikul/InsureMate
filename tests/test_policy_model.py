"""
Unit tests for the Policy model.
"""
import pytest
from datetime import datetime, timedelta
from models.policy import Policy


class TestPolicyModel:
    """Test cases for the Policy model."""
    
    def test_create_policy(self, session, sample_agent, sample_customer):
        """Test creating a new policy."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-NEW789",
            policy_type="Home Insurance",
            coverage_amount=250000.00,
            premium=1500.00,
            start_date=datetime.today().date(),
            end_date=(datetime.today() + timedelta(days=365)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.policy_id is not None
        assert policy.agent_id == sample_agent.agent_id
        assert policy.customer_id == sample_customer.customer_id
        assert policy.policy_number == "POL-NEW789"
        assert policy.policy_type == "Home Insurance"
        assert float(policy.coverage_amount) == 250000.00
        assert float(policy.premium) == 1500.00
        assert policy.policy_status == "Active"
    
    def test_policy_repr(self, sample_policy):
        """Test policy string representation."""
        assert repr(sample_policy) == '<Policy POL-TEST123>'
    
    def test_policy_is_active_true(self, sample_policy):
        """Test is_active method returns True for active policy."""
        assert sample_policy.is_active() is True
    
    def test_policy_is_active_false_expired(self, session, sample_agent, sample_customer):
        """Test is_active method returns False for expired policy."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-EXPIRED",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=(datetime.today() - timedelta(days=400)).date(),
            end_date=(datetime.today() - timedelta(days=10)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.is_active() is False
    
    def test_policy_is_active_false_status(self, session, sample_agent, sample_customer):
        """Test is_active method returns False for inactive status."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-INACTIVE",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=datetime.today().date(),
            end_date=(datetime.today() + timedelta(days=365)).date(),
            policy_status="Cancelled"
        )
        session.add(policy)
        session.commit()
        
        assert policy.is_active() is False
    
    def test_policy_days_until_renewal(self, sample_policy):
        """Test days_until_renewal calculation."""
        days = sample_policy.days_until_renewal()
        expected_days = (sample_policy.end_date - datetime.today().date()).days
        assert days == expected_days
    
    def test_policy_days_until_renewal_none(self, session, sample_agent, sample_customer):
        """Test days_until_renewal returns None when no end_date."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-NOEND",
            policy_type="Life Insurance",
            coverage_amount=500000.00,
            premium=2000.00,
            start_date=datetime.today().date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.days_until_renewal() is None
    
    def test_policy_renewal_status_ok(self, session, sample_agent, sample_customer):
        """Test renewal_status returns OK for policies far from expiry."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-OK",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=datetime.today().date(),
            end_date=(datetime.today() + timedelta(days=60)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.renewal_status() == "OK"
    
    def test_policy_renewal_status_warning(self, session, sample_agent, sample_customer):
        """Test renewal_status returns Warning for policies expiring soon."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-WARNING",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=(datetime.today() - timedelta(days=340)).date(),
            end_date=(datetime.today() + timedelta(days=20)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.renewal_status() == "Warning"
    
    def test_policy_renewal_status_critical(self, session, sample_agent, sample_customer):
        """Test renewal_status returns Critical for policies expiring very soon."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-CRITICAL",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=(datetime.today() - timedelta(days=360)).date(),
            end_date=(datetime.today() + timedelta(days=5)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.renewal_status() == "Critical"
    
    def test_policy_renewal_status_expired(self, session, sample_agent, sample_customer):
        """Test renewal_status returns Expired for expired policies."""
        policy = Policy(
            agent_id=sample_agent.agent_id,
            customer_id=sample_customer.customer_id,
            policy_number="POL-EXPIRED2",
            policy_type="Auto Insurance",
            coverage_amount=100000.00,
            premium=1200.00,
            start_date=(datetime.today() - timedelta(days=400)).date(),
            end_date=(datetime.today() - timedelta(days=10)).date(),
            policy_status="Active"
        )
        session.add(policy)
        session.commit()
        
        assert policy.renewal_status() == "Expired"
    
    def test_policy_to_dict(self, sample_policy, sample_agent, sample_customer):
        """Test converting policy to dictionary."""
        policy_dict = sample_policy.to_dict()
        
        assert policy_dict['policy_id'] == sample_policy.policy_id
        assert policy_dict['agent_id'] == sample_agent.agent_id
        assert policy_dict['customer_id'] == sample_customer.customer_id
        assert policy_dict['policy_number'] == "POL-TEST123"
        assert policy_dict['policy_type'] == "Auto Insurance"
        assert policy_dict['coverage_amount'] == 100000.00
        assert policy_dict['premium'] == 1200.00
        assert policy_dict['policy_status'] == "Active"
        assert 'start_date' in policy_dict
        assert 'end_date' in policy_dict
        assert 'is_active' in policy_dict
        assert 'days_until_renewal' in policy_dict
        assert 'renewal_status' in policy_dict
        assert policy_dict['agent_name'] == "John Doe"
        assert policy_dict['customer_name'] == "Jane Smith"
        assert 'claim_count' in policy_dict
    
    def test_policy_claims_relationship(self, sample_policy, sample_claim):
        """Test the relationship between policy and claims."""
        assert len(sample_policy.claims) == 1
        assert sample_policy.claims[0].claim_id == sample_claim.claim_id
    
    def test_policy_delete_cascades_to_claims(self, session, sample_policy, sample_claim):
        """Test that deleting a policy cascades to its claims."""
        policy_id = sample_policy.policy_id
        claim_id = sample_claim.claim_id
        
        session.delete(sample_policy)
        session.commit()
        
        # Verify policy is deleted
        from models.policy import Policy
        deleted_policy = session.get(Policy, policy_id)
        assert deleted_policy is None
        
        # Verify claim is also deleted (cascade)
        from models.claim import Claim
        deleted_claim = session.get(Claim, claim_id)
        assert deleted_claim is None
