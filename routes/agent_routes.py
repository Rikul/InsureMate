from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.agent import Agent
from models.agency import Agency
#from app import db
from models.database import db, init_db  # Import from the new database module
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

agent_bp = Blueprint('agent', __name__)

# List all agents
@agent_bp.route('/', methods=['GET'])
def index():
    search_term = request.args.get('search', '')
    
    if search_term:
        # Search by name, email, or phone
        agents = Agent.query.filter(
            or_(
                Agent.first_name.ilike(f'%{search_term}%'),
                Agent.last_name.ilike(f'%{search_term}%'),
                Agent.email.ilike(f'%{search_term}%'),
                Agent.phone.ilike(f'%{search_term}%')
            )
        ).all()
    else:
        agents = Agent.query.all()
        
    return render_template('agent/index.html', agents=agents, search_term=search_term)

# Show agent creation form
@agent_bp.route('/create', methods=['GET'])
def create_form():
    agencies = Agency.query.all()
    return render_template('agent/create.html', agencies=agencies)

# Process agent creation
@agent_bp.route('/create', methods=['POST'])
def create():
    try:
        # Create new agent from form data
        new_agent = Agent(
            agency_id=request.form.get('agency_id'),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone')
        )
        
        # Add to database
        db.session.add(new_agent)
        db.session.commit()
        
        flash('Agent created successfully!', 'success')
        return redirect(url_for('agent.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        agencies = Agency.query.all()
        flash(f'Error creating agent: {str(e)}', 'danger')
        return render_template('agent/create.html', agencies=agencies)

# Show agent details
@agent_bp.route('/<int:agent_id>', methods=['GET'])
def view(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    return render_template('agent/view.html', agent=agent)

# Show agent edit form
@agent_bp.route('/<int:agent_id>/edit', methods=['GET'])
def edit_form(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    agencies = Agency.query.all()
    return render_template('agent/edit.html', agent=agent, agencies=agencies)

# Process agent update
@agent_bp.route('/<int:agent_id>/edit', methods=['POST'])
def edit(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    
    try:
        # Update agent from form data
        agent.agency_id = request.form.get('agency_id')
        agent.first_name = request.form.get('first_name')
        agent.last_name = request.form.get('last_name')
        agent.email = request.form.get('email')
        agent.phone = request.form.get('phone')
        
        # Commit changes
        db.session.commit()
        
        flash('Agent updated successfully!', 'success')
        return redirect(url_for('agent.view', agent_id=agent.agent_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        agencies = Agency.query.all()
        flash(f'Error updating agent: {str(e)}', 'danger')
        return render_template('agent/edit.html', agent=agent, agencies=agencies)

# Delete agent
@agent_bp.route('/<int:agent_id>/delete', methods=['POST'])
def delete(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    
    try:
        db.session.delete(agent)
        db.session.commit()
        flash('Agent deleted successfully!', 'success')
        return redirect(url_for('agent.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting agent: {str(e)}', 'danger')
        return redirect(url_for('agent.view', agent_id=agent.agent_id))

# API endpoint to get agents by agency
@agent_bp.route('/api/by-agency/<int:agency_id>', methods=['GET'])
def api_agents_by_agency(agency_id):
    agents = Agent.query.filter_by(agency_id=agency_id).all()
    return jsonify([agent.to_dict() for agent in agents])

# API endpoint to get all agents
@agent_bp.route('/api/agents', methods=['GET'])
def api_agents():
    agents = Agent.query.all()
    return jsonify([agent.to_dict() for agent in agents])