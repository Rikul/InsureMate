"""
Unit tests for the Agency model.
"""
import pytest
from models.agency import Agency


class TestAgencyModel:
    """Test cases for the Agency model."""
    
    def test_create_agency(self, session):
        """Test creating a new agency."""
        agency = Agency(
            name="New Agency",
            address="789 Elm St",
            city="New City",
            state="NC",
            zip_code="99999",
            phone="555-0000",
            website="https://newagency.com"
        )
        session.add(agency)
        session.commit()
        
        assert agency.agency_id is not None
        assert agency.name == "New Agency"
        assert agency.address == "789 Elm St"
        assert agency.city == "New City"
        assert agency.state == "NC"
        assert agency.zip_code == "99999"
        assert agency.phone == "555-0000"
        assert agency.website == "https://newagency.com"
    
    def test_agency_repr(self, sample_agency):
        """Test agency string representation."""
        assert repr(sample_agency) == '<Agency Test Insurance Agency>'
    
    def test_agency_to_dict(self, sample_agency):
        """Test converting agency to dictionary."""
        agency_dict = sample_agency.to_dict()
        
        assert agency_dict['agency_id'] == sample_agency.agency_id
        assert agency_dict['name'] == "Test Insurance Agency"
        assert agency_dict['address'] == "123 Main St"
        assert agency_dict['city'] == "Test City"
        assert agency_dict['state'] == "TS"
        assert agency_dict['zip_code'] == "12345"
        assert agency_dict['phone'] == "555-1234"
        assert 'agent_count' in agency_dict
    
    def test_agency_agents_relationship(self, sample_agency, sample_agent):
        """Test the relationship between agency and agents."""
        assert len(sample_agency.agents) == 1
        assert sample_agency.agents[0].agent_id == sample_agent.agent_id
    
    def test_agency_delete_cascades_to_agents(self, session, sample_agency, sample_agent):
        """Test that deleting an agency cascades to its agents."""
        agency_id = sample_agency.agency_id
        agent_id = sample_agent.agent_id
        
        session.delete(sample_agency)
        session.commit()
        
        # Verify agency is deleted
        from models.agency import Agency
        deleted_agency = session.get(Agency, agency_id)
        assert deleted_agency is None
        
        # Verify agent is also deleted (cascade)
        from models.agent import Agent
        deleted_agent = session.get(Agent, agent_id)
        assert deleted_agent is None
