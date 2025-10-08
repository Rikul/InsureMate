from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.claim import Claim
from models.policy import Policy
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from datetime import datetime
import uuid

claim_bp = Blueprint('claim', __name__)

# List all claims
@claim_bp.route('/', methods=['GET'])
def index():
    search_term = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    query = Claim.query
    
    if search_term:
        # Search by claim number, policy number, or customer name
        query = query.join(Policy).filter(
            or_(
                Claim.claim_number.ilike(f'%{search_term}%'),
                Policy.policy_number.ilike(f'%{search_term}%')
            )
        )
    
    if status_filter:
        query = query.filter(Claim.status == status_filter)
        
    claims = query.order_by(Claim.claim_date.desc()).all()
    
    # Get unique statuses for filter dropdown
    statuses = db.session.query(Claim.status).distinct().all()
    statuses = [status[0] for status in statuses]
    
    return render_template('claim/index.html', 
                          claims=claims, 
                          search_term=search_term,
                          status_filter=status_filter,
                          statuses=statuses)

# Show claim creation form
@claim_bp.route('/create', methods=['GET'])
def create_form():
    policies = Policy.query.filter(Policy.policy_status == 'Active').all()
    return render_template('claim/create.html', policies=policies)

# Create claim for specific policy
@claim_bp.route('/policy/<int:policy_id>/create', methods=['GET'])
def create_for_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    return render_template('claim/create.html', policy=policy)

# Process claim creation
@claim_bp.route('/create', methods=['POST'])
def create():
    try:
        # Validate required fields
        policy_id = request.form.get('policy_id')
        if not policy_id:
            flash('Policy is required', 'danger')
            policies = Policy.query.filter(Policy.policy_status == 'Active').all()
            return render_template('claim/create.html', policies=policies)
        
        incident_date = request.form.get('incident_date')
        if not incident_date:
            flash('Incident date is required', 'danger')
            policies = Policy.query.filter(Policy.policy_status == 'Active').all()
            return render_template('claim/create.html', policies=policies)
        
        # Generate unique claim number
        claim_number = f"CLM-{uuid.uuid4().hex[:8].upper()}"
        
        # Create new claim
        new_claim = Claim(
            policy_id=policy_id,
            claim_number=claim_number,
            claim_date=datetime.today().date(),
            incident_date=datetime.strptime(incident_date, '%Y-%m-%d').date(),
            description=request.form.get('description', '').strip(),
            claim_amount=request.form.get('claim_amount', 0),
            status='Open'
        )
        
        # Add to database
        db.session.add(new_claim)
        db.session.commit()
        
        flash('Claim created successfully!', 'success')
        return redirect(url_for('claim.view', claim_id=new_claim.claim_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error creating claim: {str(e)}', 'danger')
        policies = Policy.query.filter(Policy.policy_status == 'Active').all()
        return render_template('claim/create.html', policies=policies)

# Show claim details
@claim_bp.route('/<int:claim_id>', methods=['GET'])
def view(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    return render_template('claim/view.html', claim=claim)

# Show claim edit form
@claim_bp.route('/<int:claim_id>/edit', methods=['GET'])
def edit_form(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    return render_template('claim/edit.html', claim=claim)

# Process claim update
@claim_bp.route('/<int:claim_id>/edit', methods=['POST'])
def edit(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    
    try:
        # Update claim
        claim.description = request.form.get('description', '').strip()
        claim.claim_amount = request.form.get('claim_amount', 0)
        claim.status = request.form.get('status')
        
        # If status is closed/settled, update resolution fields
        if claim.status in ['Settled', 'Denied', 'Closed', 'Withdrawn']:
            claim.resolution_date = datetime.today().date()
            if claim.status == 'Settled':
                claim.settlement_amount = request.form.get('settlement_amount', 0)
        
        # Commit changes
        db.session.commit()
        
        flash('Claim updated successfully!', 'success')
        return redirect(url_for('claim.view', claim_id=claim.claim_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error updating claim: {str(e)}', 'danger')
        return render_template('claim/edit.html', claim=claim)

# Delete claim
@claim_bp.route('/<int:claim_id>/delete', methods=['POST'])
def delete(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    
    try:
        db.session.delete(claim)
        db.session.commit()
        flash('Claim deleted successfully!', 'success')
        return redirect(url_for('claim.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting claim: {str(e)}', 'danger')
        return redirect(url_for('claim.view', claim_id=claim.claim_id))

# API endpoint to get claims for a policy
@claim_bp.route('/api/policy/<int:policy_id>/claims', methods=['GET'])
def api_policy_claims(policy_id):
    claims = Claim.query.filter_by(policy_id=policy_id).all()
    return jsonify([claim.to_dict() for claim in claims])

# API endpoint to get all claims
@claim_bp.route('/api/claims', methods=['GET'])
def api_claims():
    claims = Claim.query.all()
    return jsonify([claim.to_dict() for claim in claims]) 