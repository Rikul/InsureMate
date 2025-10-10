from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.customer import Customer
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from datetime import datetime

customer_bp = Blueprint('customer', __name__)

# List all customers
@customer_bp.route('/', methods=['GET'])
def index():
    search_term = request.args.get('search', '')
    
    if search_term:
        # Search by name, email, or phone
        customers = Customer.query.filter(
            or_(
                Customer.first_name.ilike(f'%{search_term}%'),
                Customer.last_name.ilike(f'%{search_term}%'),
                Customer.email.ilike(f'%{search_term}%'),
                Customer.phone.ilike(f'%{search_term}%')
            )
        ).all()
    else:
        customers = Customer.query.all()
        
    return render_template('customer/index.html', customers=customers, search_term=search_term)

# Show customer creation form
@customer_bp.route('/create', methods=['GET'])
def create_form():
    return render_template('customer/create.html')

# Process customer creation
@customer_bp.route('/create', methods=['POST'])
def create():
    try:
        # Validate required fields
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if not first_name or first_name.strip() == '':
            flash('First name is required', 'danger')
            return render_template('customer/create.html')
        
        if not last_name or last_name.strip() == '':
            flash('Last name is required', 'danger')
            return render_template('customer/create.html')
        
        # Parse date of birth if provided
        dob_str = request.form.get('date_of_birth')
        dob = None
        if dob_str:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        
        # Create new customer from form data
        new_customer = Customer(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            date_of_birth=dob,
            email=request.form.get('email', '').strip(),
            phone=request.form.get('phone', '').strip(),
            address=request.form.get('address', '').strip(),
            city=request.form.get('city', '').strip(),
            state=request.form.get('state', '').strip(),
            zip_code=request.form.get('zip_code', '').strip()
        )
        
        # Add to database
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Customer created successfully!', 'success')
        return redirect(url_for('customer.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error creating customer: {str(e)}', 'danger')
        return render_template('customer/create.html')

# Show customer details
@customer_bp.route('/<int:customer_id>', methods=['GET'])
def view(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customer/view.html', customer=customer)

# Show customer edit form
@customer_bp.route('/<int:customer_id>/edit', methods=['GET'])
def edit_form(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customer/edit.html', customer=customer)

# Process customer update
@customer_bp.route('/<int:customer_id>/edit', methods=['POST'])
def edit(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    try:
        # Validate required fields
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if not first_name or first_name.strip() == '':
            flash('First name is required', 'danger')
            return render_template('customer/edit.html', customer=customer)
        
        if not last_name or last_name.strip() == '':
            flash('Last name is required', 'danger')
            return render_template('customer/edit.html', customer=customer)
        
        # Parse date of birth if provided
        dob_str = request.form.get('date_of_birth')
        if dob_str:
            customer.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        
        # Update customer from form data
        customer.first_name = first_name.strip()
        customer.last_name = last_name.strip()
        customer.email = request.form.get('email', '').strip()
        customer.phone = request.form.get('phone', '').strip()
        customer.address = request.form.get('address', '').strip()
        customer.city = request.form.get('city', '').strip()
        customer.state = request.form.get('state', '').strip()
        customer.zip_code = request.form.get('zip_code', '').strip()
        
        # Commit changes
        db.session.commit()
        
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.view', customer_id=customer.customer_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error updating customer: {str(e)}', 'danger')
        return render_template('customer/edit.html', customer=customer)

# Delete customer
@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
def delete(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
        return redirect(url_for('customer.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting customer: {str(e)}', 'danger')
        return redirect(url_for('customer.view', customer_id=customer.customer_id))

# API endpoint to get all customers
@customer_bp.route('/api/customers', methods=['GET'])
def api_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])