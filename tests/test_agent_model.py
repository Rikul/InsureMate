"""
Unit tests for the Agent model.
"""
import pytest
from models.agent import Agent


class TestAgentModel:
    """Test cases for the Agent model."""
    
    def test_create_agent(self, session, sample_agency):
        """Test creating a new agent."""
        agent = Agent(
            agency_id=sample_agency.agency_id,
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@test.com",
            phone="555-1111"
        )
        session.add(agent)
        session.commit()
        
        assert agent.agent_id is not None
        assert agent.agency_id == sample_agency.agency_id
        assert agent.first_name == "Alice"
        assert agent.last_name == "Johnson"
        assert agent.email == "alice.johnson@test.com"
        assert agent.phone == "555-1111"
    
    def test_agent_repr(self, sample_agent):
        """Test agent string representation."""
        assert repr(sample_agent) == '<Agent John Doe>'
    
    def test_agent_full_name(self, sample_agent):
        """Test agent full_name method."""
        assert sample_agent.full_name() == "John Doe"
    
    def test_agent_to_dict(self, sample_agent, sample_agency):
        """Test converting agent to dictionary."""
        agent_dict = sample_agent.to_dict()
        
        assert agent_dict['agent_id'] == sample_agent.agent_id
        assert agent_dict['agency_id'] == sample_agency.agency_id
        assert agent_dict['first_name'] == "John"
        assert agent_dict['last_name'] == "Doe"
        assert agent_dict['email'] == "john.doe@testinsurance.com"
        assert agent_dict['phone'] == "555-5678"
        assert agent_dict['full_name'] == "John Doe"
        assert agent_dict['agency_name'] == "Test Insurance Agency"
        assert 'policy_count' in agent_dict
    
    def test_agent_agency_relationship(self, sample_agent, sample_agency):
        """Test the relationship between agent and agency."""
        assert sample_agent.agency == sample_agency
        assert sample_agent.agency.name == "Test Insurance Agency"
    
    def test_agent_policies_relationship(self, sample_agent, sample_policy):
        """Test the relationship between agent and policies."""
        assert len(sample_agent.policies) == 1
        assert sample_agent.policies[0].policy_id == sample_policy.policy_id
    
    def test_agent_delete_cascades_to_policies(self, session, sample_agent, sample_policy):
        """Test that deleting an agent cascades to its policies."""
        agent_id = sample_agent.agent_id
        policy_id = sample_policy.policy_id
        
        session.delete(sample_agent)
        session.commit()
        
        # Verify agent is deleted
        from models.agent import Agent
        deleted_agent = session.get(Agent, agent_id)
        assert deleted_agent is None
        
        # Verify policy is also deleted (cascade)
        from models.policy import Policy
        deleted_policy = session.get(Policy, policy_id)
        assert deleted_policy is None
