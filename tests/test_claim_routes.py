"""
Integration tests for claim routes.
"""
import pytest
import json
from datetime import datetime, timedelta


class TestClaimRoutes:
    """Test cases for claim routes."""
    
    def test_claim_index(self, client, sample_claim):
        """Test the claims index page."""
        response = client.get('/claims/')
        assert response.status_code == 200
        assert b'CLM-TEST456' in response.data
    
    def test_claim_index_search(self, client, sample_claim):
        """Test searching claims."""
        response = client.get('/claims/?search=CLM-TEST456')
        assert response.status_code == 200
        assert b'CLM-TEST456' in response.data
    
    def test_claim_create_form(self, client, sample_policy):
        """Test the claim create form page."""
        response = client.get('/claims/create')
        assert response.status_code == 200
        assert b'Create Claim' in response.data or b'File Claim' in response.data or b'New Claim' in response.data
    
    def test_claim_create_for_policy(self, client, sample_policy):
        """Test the claim create form for a specific policy."""
        response = client.get(f'/claims/policy/{sample_policy.policy_id}/create')
        assert response.status_code == 200
        assert b'POL-TEST123' in response.data or b'claim' in response.data.lower()
    
    def test_claim_create_success(self, client, session, sample_policy):
        """Test creating a new claim."""
        response = client.post('/claims/create', data={
            'policy_id': sample_policy.policy_id,
            'incident_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'description': 'New test claim description',
            'claim_amount': '2500.00',
            'status': 'Open'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_claim_create_missing_policy(self, client):
        """Test creating a claim without a policy."""
        response = client.post('/claims/create', data={
            'incident_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'description': 'Test description',
            'claim_amount': '2500.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'policy' in response.data.lower()
    
    def test_claim_create_missing_incident_date(self, client, sample_policy):
        """Test creating a claim without incident date."""
        response = client.post('/claims/create', data={
            'policy_id': sample_policy.policy_id,
            'description': 'Test description',
            'claim_amount': '2500.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'date' in response.data.lower()
    
    def test_claim_view(self, client, sample_claim):
        """Test viewing a claim."""
        response = client.get(f'/claims/{sample_claim.claim_id}')
        assert response.status_code == 200
        assert b'CLM-TEST456' in response.data
    
    def test_claim_view_not_found(self, client):
        """Test viewing a non-existent claim."""
        response = client.get('/claims/99999')
        assert response.status_code == 404
    
    def test_claim_edit_form(self, client, sample_claim):
        """Test the claim edit form page."""
        response = client.get(f'/claims/{sample_claim.claim_id}/edit')
        assert response.status_code == 200
        assert b'CLM-TEST456' in response.data
    
    def test_claim_edit_success(self, client, sample_claim):
        """Test editing a claim."""
        response = client.post(f'/claims/{sample_claim.claim_id}/edit', data={
            'description': 'Updated claim description',
            'claim_amount': '6000.00',
            'status': 'In Progress'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_claim_delete(self, client, session, sample_claim):
        """Test deleting a claim."""
        claim_id = sample_claim.claim_id
        response = client.post(f'/claims/{claim_id}/delete', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify claim is deleted
        from models.claim import Claim
        deleted_claim = session.get(Claim, claim_id)
        assert deleted_claim is None
    
    def test_claim_api_list(self, client, sample_claim):
        """Test the API endpoint for listing claims."""
        response = client.get('/claims/api/claims')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Find our test claim in the response
        test_claim = next((c for c in data if c['claim_number'] == 'CLM-TEST456'), None)
        assert test_claim is not None
        assert test_claim['status'] == 'Open'
    
    def test_claim_api_policy_claims(self, client, sample_policy, sample_claim):
        """Test the API endpoint for listing claims by policy."""
        response = client.get(f'/claims/api/policy/{sample_policy.policy_id}/claims')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verify all claims belong to the policy
        for claim in data:
            assert claim['policy_id'] == sample_policy.policy_id
