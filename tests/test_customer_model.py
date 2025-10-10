"""
Unit tests for the Customer model.
"""
import pytest
from datetime import datetime
from models.customer import Customer


class TestCustomerModel:
    """Test cases for the Customer model."""
    
    def test_create_customer(self, session):
        """Test creating a new customer."""
        customer = Customer(
            first_name="Bob",
            last_name="Brown",
            date_of_birth=datetime(1985, 5, 15).date(),
            email="bob.brown@example.com",
            phone="555-2222",
            address="321 Pine Rd",
            city="Pine City",
            state="PC",
            zip_code="11111"
        )
        session.add(customer)
        session.commit()
        
        assert customer.customer_id is not None
        assert customer.first_name == "Bob"
        assert customer.last_name == "Brown"
        assert customer.date_of_birth == datetime(1985, 5, 15).date()
        assert customer.email == "bob.brown@example.com"
        assert customer.phone == "555-2222"
        assert customer.address == "321 Pine Rd"
        assert customer.city == "Pine City"
        assert customer.state == "PC"
        assert customer.zip_code == "11111"
    
    def test_customer_repr(self, sample_customer):
        """Test customer string representation."""
        assert repr(sample_customer) == '<Customer Jane Smith>'
    
    def test_customer_full_name(self, sample_customer):
        """Test customer full_name method."""
        assert sample_customer.full_name() == "Jane Smith"
    
    def test_customer_full_address(self, sample_customer):
        """Test customer full_address method."""
        full_address = sample_customer.full_address()
        assert "456 Oak Ave" in full_address
        assert "Test Town" in full_address
        assert "TS" in full_address
        assert "54321" in full_address
    
    def test_customer_full_address_with_missing_fields(self, session):
        """Test customer full_address method with missing fields."""
        customer = Customer(
            first_name="Charlie",
            last_name="Davis",
            city="Davis City"
        )
        session.add(customer)
        session.commit()
        
        assert customer.full_address() == "Davis City"
    
    def test_customer_age(self, sample_customer):
        """Test customer age calculation."""
        age = sample_customer.age()
        # Customer born in 1990, so age should be current year - 1990
        expected_age = datetime.today().year - 1990
        # Adjust for birthday not yet occurred this year
        if (datetime.today().month, datetime.today().day) < (1, 1):
            expected_age -= 1
        assert age == expected_age
    
    def test_customer_age_none_when_no_dob(self, session):
        """Test that age is None when date of birth is not set."""
        customer = Customer(
            first_name="Charlie",
            last_name="Davis"
        )
        session.add(customer)
        session.commit()
        
        assert customer.age() is None
    
    def test_customer_to_dict(self, sample_customer):
        """Test converting customer to dictionary."""
        customer_dict = sample_customer.to_dict()
        
        assert customer_dict['customer_id'] == sample_customer.customer_id
        assert customer_dict['first_name'] == "Jane"
        assert customer_dict['last_name'] == "Smith"
        assert customer_dict['date_of_birth'] == "1990-01-01"
        assert customer_dict['email'] == "jane.smith@example.com"
        assert customer_dict['phone'] == "555-9012"
        assert customer_dict['address'] == "456 Oak Ave"
        assert customer_dict['city'] == "Test Town"
        assert customer_dict['state'] == "TS"
        assert customer_dict['zip_code'] == "54321"
        assert customer_dict['full_name'] == "Jane Smith"
        assert 'full_address' in customer_dict
        assert 'age' in customer_dict
        assert 'policy_count' in customer_dict
    
    def test_customer_policies_relationship(self, sample_customer, sample_policy):
        """Test the relationship between customer and policies."""
        assert len(sample_customer.policies) == 1
        assert sample_customer.policies[0].policy_id == sample_policy.policy_id
    
    def test_customer_delete_cascades_to_policies(self, session, sample_customer, sample_policy):
        """Test that deleting a customer cascades to its policies."""
        customer_id = sample_customer.customer_id
        policy_id = sample_policy.policy_id
        
        session.delete(sample_customer)
        session.commit()
        
        # Verify customer is deleted
        from models.customer import Customer
        deleted_customer = session.get(Customer, customer_id)
        assert deleted_customer is None
        
        # Verify policy is also deleted (cascade)
        from models.policy import Policy
        deleted_policy = session.get(Policy, policy_id)
        assert deleted_policy is None
