from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from models.policy import Policy
from models.agent import Agent
from models.customer import Customer
from models.database import db

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from datetime import datetime

policy_bp = Blueprint('policy', __name__)

# List all policies
@policy_bp.route('/', methods=['GET'])
def index():
    search_term = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('ITEMS_PER_PAGE', 10)

    query = Policy.query
    
    if search_term:
        # Search by policy number, policy type, or customer/agent names
        query = query.join(Customer).join(Agent).filter(
            or_(
                Policy.policy_number.ilike(f'%{search_term}%'),
                Policy.policy_type.ilike(f'%{search_term}%'),
                Customer.first_name.ilike(f'%{search_term}%'),
                Customer.last_name.ilike(f'%{search_term}%'),
                Agent.first_name.ilike(f'%{search_term}%'),
                Agent.last_name.ilike(f'%{search_term}%')
            )
        )

    if status_filter:
        query = query.filter(Policy.policy_status == status_filter)

    policies_query = query.order_by(Policy.start_date.desc())
    pagination = policies_query.paginate(page=page, per_page=per_page, error_out=False)
    policies = pagination.items

    start_index = (pagination.page - 1) * pagination.per_page + 1 if pagination.total else 0
    end_index = min(pagination.page * pagination.per_page, pagination.total) if pagination.total else 0
    
    # Get unique statuses for filter dropdown
    statuses = db.session.query(Policy.policy_status).distinct().all()
    statuses = [status[0] for status in statuses]
    
    return render_template('policy/index.html',
                          policies=policies,
                          search_term=search_term,
                          status_filter=status_filter,
                          statuses=statuses,
                          pagination=pagination,
                          start_index=start_index,
                          end_index=end_index)

# Show policy creation form
@policy_bp.route('/create', methods=['GET'])
def create_form():
    agents = Agent.query.all()
    customers = Customer.query.all()
    return render_template('policy/create.html', agents=agents, customers=customers)

# Process policy creation
@policy_bp.route('/create', methods=['POST'])
def create():
    try:
        # Validate required fields
        agent_id = request.form.get('agent_id')
        customer_id = request.form.get('customer_id')
        policy_number = request.form.get('policy_number')
        policy_type = request.form.get('policy_type')
        start_date_str = request.form.get('start_date')
        
        if not agent_id:
            flash('Agent is required', 'danger')
            agents = Agent.query.all()
            customers = Customer.query.all()
            return render_template('policy/create.html', agents=agents, customers=customers)
        
        if not customer_id:
            flash('Customer is required', 'danger')
            agents = Agent.query.all()
            customers = Customer.query.all()
            return render_template('policy/create.html', agents=agents, customers=customers)
        
        if not policy_number or policy_number.strip() == '':
            flash('Policy number is required', 'danger')
            agents = Agent.query.all()
            customers = Customer.query.all()
            return render_template('policy/create.html', agents=agents, customers=customers)
        
        if not policy_type or policy_type.strip() == '':
            flash('Policy type is required', 'danger')
            agents = Agent.query.all()
            customers = Customer.query.all()
            return render_template('policy/create.html', agents=agents, customers=customers)
        
        if not start_date_str:
            flash('Start date is required', 'danger')
            agents = Agent.query.all()
            customers = Customer.query.all()
            return render_template('policy/create.html', agents=agents, customers=customers)
        
        # Parse dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        end_date_str = request.form.get('end_date')
        end_date = None
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Parse decimal values
        coverage_amount = request.form.get('coverage_amount', 0)
        premium = request.form.get('premium', 0)
        
        # Create new policy from form data
        new_policy = Policy(
            agent_id=agent_id,
            customer_id=customer_id,
            policy_number=policy_number.strip(),
            policy_type=policy_type.strip(),
            coverage_amount=coverage_amount,
            premium=premium,
            start_date=start_date,
            end_date=end_date,
            policy_status=request.form.get('policy_status', 'Active')
        )
        
        # Add to database
        db.session.add(new_policy)
        db.session.commit()
        
        flash('Policy created successfully!', 'success')
        return redirect(url_for('policy.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        agents = Agent.query.all()
        customers = Customer.query.all()
        flash(f'Error creating policy: {str(e)}', 'danger')
        return render_template('policy/create.html', agents=agents, customers=customers)

# Show policy details
@policy_bp.route('/<int:policy_id>', methods=['GET'])
def view(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    return render_template('policy/view.html', policy=policy)

# Show policy edit form
@policy_bp.route('/<int:policy_id>/edit', methods=['GET'])
def edit_form(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    agents = Agent.query.all()
    customers = Customer.query.all()
    return render_template('policy/edit.html', policy=policy, agents=agents, customers=customers)

# Process policy update
@policy_bp.route('/<int:policy_id>/edit', methods=['POST'])
def edit(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    
    try:
        # Parse dates
        start_date_str = request.form.get('start_date')
        if start_date_str:
            policy.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        end_date_str = request.form.get('end_date')
        if end_date_str:
            policy.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            policy.end_date = None
        
        # Update policy from form data
        policy.agent_id = request.form.get('agent_id')
        policy.customer_id = request.form.get('customer_id')
        policy.policy_number = request.form.get('policy_number')
        policy.policy_type = request.form.get('policy_type')
        policy.coverage_amount = request.form.get('coverage_amount', 0)
        policy.premium = request.form.get('premium', 0)
        policy.policy_status = request.form.get('policy_status')
        
        # Commit changes
        db.session.commit()
        
        flash('Policy updated successfully!', 'success')
        return redirect(url_for('policy.view', policy_id=policy.policy_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        agents = Agent.query.all()
        customers = Customer.query.all()
        flash(f'Error updating policy: {str(e)}', 'danger')
        return render_template('policy/edit.html', policy=policy, agents=agents, customers=customers)

# Delete policy
@policy_bp.route('/<int:policy_id>/delete', methods=['POST'])
def delete(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    
    try:
        db.session.delete(policy)
        db.session.commit()
        flash('Policy deleted successfully!', 'success')
        return redirect(url_for('policy.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting policy: {str(e)}', 'danger')
        return redirect(url_for('policy.view', policy_id=policy.policy_id))

# API endpoint to get policies
@policy_bp.route('/api/policies', methods=['GET'])
def api_policies():
    policies = Policy.query.all()
    return jsonify([policy.to_dict() for policy in policies])

# API endpoint to get policies for a specific customer
@policy_bp.route('/api/by-customer/<int:customer_id>', methods=['GET'])
def api_policies_by_customer(customer_id):
    policies = Policy.query.filter_by(customer_id=customer_id).all()
    return jsonify([policy.to_dict() for policy in policies])

# API endpoint to get policies for a specific agent
@policy_bp.route('/api/by-agent/<int:agent_id>', methods=['GET'])
def api_policies_by_agent(agent_id):
    policies = Policy.query.filter_by(agent_id=agent_id).all()
    return jsonify([policy.to_dict() for policy in policies])