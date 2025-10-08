// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Confirm deletes
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Dynamic form handling for agency selection in agent forms
    const agencySelect = document.getElementById('agency_id');
    if (agencySelect) {
        // If the form has an agency dropdown, set up AJAX to load agents
        agencySelect.addEventListener('change', function() {
            const agencyId = this.value;
            if (!agencyId) return;

            // Make AJAX request to get agents for this agency
            fetch(`/agents/api/by-agency/${agencyId}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Agents data:', data);
                    // Clear and populate agent dropdown if it exists
                    const agentSelect = document.getElementById('agent_id');
                    if (agentSelect) {
                        // Clear existing options
                        agentSelect.innerHTML = '<option value="" selected disabled>Select Agent</option>';
                        
                        // Add new options
                        data.forEach(agent => {
                            const option = document.createElement('option');
                            option.value = agent.agent_id;
                            option.textContent = `${agent.first_name} ${agent.last_name}`;
                            agentSelect.appendChild(option);
                        });
                        
                        // Enable the select if it was disabled
                        agentSelect.disabled = false;
                    }
                })
                .catch(error => console.error('Error loading agents:', error));
        });
    }

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('.currency-input');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Format date inputs to show date in local format
    const dateDisplayElements = document.querySelectorAll('.date-display');
    dateDisplayElements.forEach(element => {
        const dateString = element.textContent.trim();
        if (dateString) {
            try {
                const date = new Date(dateString);
                element.textContent = date.toLocaleDateString();
            } catch (e) {
                console.error('Error formatting date:', e);
            }
        }
    });
});

// Function to generate policy number
function generatePolicyNumber() {
    const prefix = 'POL';
    const timestamp = new Date().getTime().toString().slice(-6);
    const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    return `${prefix}-${timestamp}${random}`;
}

// Set policy number when clicking the generate button
document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'generate-policy-number') {
        e.preventDefault();
        document.getElementById('policy_number').value = generatePolicyNumber();
    }
});