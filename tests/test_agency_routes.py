"""
Integration tests for agency routes.
"""
import pytest
import json


class TestAgencyRoutes:
    """Test cases for agency routes."""
    
    def test_agency_index(self, client, sample_agency):
        """Test the agencies index page."""
        response = client.get('/agencies/')
        assert response.status_code == 200
        assert b'Test Insurance Agency' in response.data
    
    def test_agency_index_search(self, client, sample_agency):
        """Test searching agencies."""
        response = client.get('/agencies/?search=Test')
        assert response.status_code == 200
        assert b'Test Insurance Agency' in response.data
    
    def test_agency_index_search_no_results(self, client, sample_agency):
        """Test searching agencies with no results."""
        response = client.get('/agencies/?search=NonExistent')
        assert response.status_code == 200
        assert b'Test Insurance Agency' not in response.data
    
    def test_agency_create_form(self, client):
        """Test the agency create form page."""
        response = client.get('/agencies/create')
        assert response.status_code == 200
        assert b'Create Agency' in response.data or b'New Agency' in response.data
    
    def test_agency_create_success(self, client, session):
        """Test creating a new agency."""
        response = client.post('/agencies/create', data={
            'name': 'New Test Agency',
            'address': '999 New St',
            'city': 'New City',
            'state': 'NC',
            'zip_code': '99999',
            'phone': '555-9999',
            'website': 'https://newtest.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'New Test Agency' in response.data or b'success' in response.data.lower()
    
    def test_agency_create_missing_name(self, client):
        """Test creating an agency without a name."""
        response = client.post('/agencies/create', data={
            'address': '999 New St',
            'city': 'New City'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'name' in response.data.lower()
    
    def test_agency_view(self, client, sample_agency):
        """Test viewing an agency."""
        response = client.get(f'/agencies/{sample_agency.agency_id}')
        assert response.status_code == 200
        assert b'Test Insurance Agency' in response.data
    
    def test_agency_view_not_found(self, client):
        """Test viewing a non-existent agency."""
        response = client.get('/agencies/99999')
        assert response.status_code == 404
    
    def test_agency_edit_form(self, client, sample_agency):
        """Test the agency edit form page."""
        response = client.get(f'/agencies/{sample_agency.agency_id}/edit')
        assert response.status_code == 200
        assert b'Test Insurance Agency' in response.data
    
    def test_agency_edit_success(self, client, sample_agency):
        """Test editing an agency."""
        response = client.post(f'/agencies/{sample_agency.agency_id}/edit', data={
            'name': 'Updated Agency Name',
            'address': '123 Main St',
            'city': 'Test City',
            'state': 'TS',
            'zip_code': '12345',
            'phone': '555-1234',
            'website': 'https://updated.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Updated Agency Name' in response.data or b'success' in response.data.lower()
    
    def test_agency_edit_missing_name(self, client, sample_agency):
        """Test editing an agency without a name."""
        response = client.post(f'/agencies/{sample_agency.agency_id}/edit', data={
            'name': '',
            'address': '123 Main St'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'name' in response.data.lower()
    
    def test_agency_delete(self, client, session, sample_agency):
        """Test deleting an agency."""
        agency_id = sample_agency.agency_id
        response = client.post(f'/agencies/{agency_id}/delete', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify agency is deleted
        from models.agency import Agency
        deleted_agency = session.get(Agency, agency_id)
        assert deleted_agency is None
    
    def test_agency_api_list(self, client, sample_agency):
        """Test the API endpoint for listing agencies."""
        response = client.get('/agencies/api/agencies')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Find our test agency in the response
        test_agency = next((a for a in data if a['name'] == 'Test Insurance Agency'), None)
        assert test_agency is not None
        assert test_agency['city'] == 'Test City'
