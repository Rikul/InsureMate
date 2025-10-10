from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from models.agency import Agency
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

agency_bp = Blueprint('agency', __name__)

# List all agencies
@agency_bp.route('/', methods=['GET'])
def index():
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    per_page = current_app.config.get('ITEMS_PER_PAGE', 10)

    query = Agency.query

    if search_term:
        # Search by name, address, city, state, or phone
        query = query.filter(
            or_(
                Agency.name.ilike(f'%{search_term}%'),
                Agency.address.ilike(f'%{search_term}%'),
                Agency.city.ilike(f'%{search_term}%'),
                Agency.state.ilike(f'%{search_term}%'),
                Agency.phone.ilike(f'%{search_term}%')
            )
        )

    pagination = query.order_by(Agency.agency_id.asc()).paginate(page=page, per_page=per_page, error_out=False)

    if pagination.total and page > pagination.pages:
        page = pagination.pages
        pagination = query.order_by(Agency.agency_id.asc()).paginate(page=page, per_page=per_page, error_out=False)

    agencies = pagination.items

    if pagination.total and pagination.items:
        start_index = (pagination.page - 1) * pagination.per_page + 1
        end_index = start_index + len(pagination.items) - 1
    else:
        start_index = 0
        end_index = 0

    return render_template(
        'agency/index.html',
        agencies=agencies,
        search_term=search_term,
        pagination=pagination,
        start_index=start_index,
        end_index=end_index
    )

# Show agency creation form
@agency_bp.route('/create', methods=['GET'])
def create_form():
    return render_template('agency/create.html')

# Process agency creation
@agency_bp.route('/create', methods=['POST'])
def create():
    try:
        # Validate required fields
        name = request.form.get('name')
        if not name or name.strip() == '':
            flash('Agency name is required', 'danger')
            return render_template('agency/create.html')
            
        # Create new agency from form data
        new_agency = Agency(
            name=name.strip(),
            address=request.form.get('address', '').strip(),
            city=request.form.get('city', '').strip(),
            state=request.form.get('state', '').strip(),
            zip_code=request.form.get('zip_code', '').strip(),
            phone=request.form.get('phone', '').strip(),
            website=request.form.get('website', '').strip()
        )
        
        # Add to database
        db.session.add(new_agency)
        db.session.commit()
        
        flash('Agency created successfully!', 'success')
        return redirect(url_for('agency.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error creating agency: {str(e)}', 'danger')
        return render_template('agency/create.html')

# Show agency details
@agency_bp.route('/<int:agency_id>', methods=['GET'])
def view(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    return render_template('agency/view.html', agency=agency)

# Show agency edit form
@agency_bp.route('/<int:agency_id>/edit', methods=['GET'])
def edit_form(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    return render_template('agency/edit.html', agency=agency)

# Process agency update
@agency_bp.route('/<int:agency_id>/edit', methods=['POST'])
def edit(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    
    try:
        # Validate required fields
        name = request.form.get('name')
        if not name or name.strip() == '':
            flash('Agency name is required', 'danger')
            return render_template('agency/edit.html', agency=agency)
            
        # Update agency from form data
        agency.name = name.strip()
        agency.address = request.form.get('address', '').strip()
        agency.city = request.form.get('city', '').strip()
        agency.state = request.form.get('state', '').strip()
        agency.zip_code = request.form.get('zip_code', '').strip()
        agency.phone = request.form.get('phone', '').strip()
        agency.website = request.form.get('website', '').strip()
        
        # Commit changes
        db.session.commit()
        
        flash('Agency updated successfully!', 'success')
        return redirect(url_for('agency.view', agency_id=agency.agency_id))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error updating agency: {str(e)}', 'danger')
        return render_template('agency/edit.html', agency=agency)

# Delete agency
@agency_bp.route('/<int:agency_id>/delete', methods=['POST'])
def delete(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    
    try:
        db.session.delete(agency)
        db.session.commit()
        flash('Agency deleted successfully!', 'success')
        return redirect(url_for('agency.index'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting agency: {str(e)}', 'danger')
        return redirect(url_for('agency.view', agency_id=agency.agency_id))

# API endpoint to get agency data
@agency_bp.route('/api/agencies', methods=['GET'])
def api_agencies():
    agencies = Agency.query.all()
    return jsonify([agency.to_dict() for agency in agencies])