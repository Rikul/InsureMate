"""
Integration tests for the main application.
"""
import pytest


class TestMainApp:
    """Test cases for the main application."""
    
    def test_app_exists(self, app):
        """Test that the app exists."""
        assert app is not None
    
    def test_app_is_testing(self, app):
        """Test that the app is in testing mode."""
        assert app.config['TESTING'] is True
    
    def test_index_page(self, client):
        """Test the index/dashboard page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Insurance' in response.data
    
    def test_index_with_data(self, client, sample_agency, sample_agent, 
                            sample_customer, sample_policy, sample_claim):
        """Test the dashboard with sample data."""
        response = client.get('/')
        assert response.status_code == 200
        # Dashboard should display counts
        assert b'Dashboard' in response.data or b'Insurance' in response.data
    
    def test_404_error_handler(self, client):
        """Test the 404 error handler."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        assert b'404' in response.data or b'not found' in response.data.lower()
    
    def test_context_processor_inject_now(self, app):
        """Test that the context processor injects 'now'."""
        with app.test_request_context():
            # Get the context processors
            processors = app.template_context_processors[None]
            context = {}
            for processor in processors:
                context.update(processor())
            
            assert 'now' in context
            assert context['now'] is not None
