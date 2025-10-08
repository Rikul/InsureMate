# Insurance Management System

A comprehensive Flask-based web application for managing insurance agencies, agents, customers, policies, and claims.

## Features

- **Agency Management**: Create, view, edit, and delete insurance agencies
- **Agent Management**: Manage insurance agents and their assignments to agencies
- **Customer Management**: Handle customer information and contact details
- **Policy Management**: Create and manage insurance policies with various types and coverage
- **Claims Management**: Track and process insurance claims with status updates
- **Dashboard**: Overview of key metrics and recent activities
- **Search & Filter**: Advanced search and filtering capabilities across all entities
- **Responsive Design**: Modern, mobile-friendly user interface using Bootstrap 5

## Technology Stack

- **Backend**: Python 3.9+, Flask
- **Database**: SQLAlchemy (SQLite by default)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Icons**: Bootstrap Icons
- **Migration**: Flask-Migrate

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd insurance-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Usage

### Dashboard
- View summary statistics for agencies, agents, customers, policies, and claims
- Monitor recent activities and upcoming policy renewals
- Access quick action buttons for common tasks

### Managing Agencies
- Add new insurance agencies with contact information
- View agency details and associated agents
- Edit agency information
- Search agencies by name, location, or contact details

### Managing Agents
- Create agent profiles linked to agencies
- View agent performance and assigned policies
- Update agent information
- Filter agents by agency or search by name/contact

### Managing Customers
- Register new customers with comprehensive contact details
- Track customer policies and claims history
- Update customer information
- Search customers by name, email, or phone

### Managing Policies
- Create new insurance policies with detailed coverage information
- Link policies to customers and agents
- Track policy status and renewal dates
- Search policies by number, type, or customer/agent names
- Filter policies by status

### Managing Claims
- File new claims against existing policies
- Track claim status from filing to resolution
- Update claim information and settlement amounts
- Search claims by claim number or policy
- Filter claims by status

## Database Schema

The application uses the following main entities:

- **Agency**: Insurance agencies with contact information
- **Agent**: Insurance agents linked to agencies
- **Customer**: Policy holders with personal information
- **Policy**: Insurance policies with coverage details
- **Claim**: Claims filed against policies

## API Endpoints

The application provides RESTful API endpoints for each entity:

- `/agencies/api/agencies` - Get all agencies
- `/agents/api/agents` - Get all agents
- `/agents/api/by-agency/<agency_id>` - Get agents by agency
- `/customers/api/customers` - Get all customers
- `/policies/api/policies` - Get all policies
- `/policies/api/by-customer/<customer_id>` - Get policies by customer
- `/policies/api/by-agent/<agent_id>` - Get policies by agent
- `/claims/api/claims` - Get all claims
- `/claims/api/policy/<policy_id>/claims` - Get claims by policy

## Configuration

The application can be configured by modifying `config.py`:

- Database URL
- Secret key for sessions
- Debug mode settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please create an issue in the repository.