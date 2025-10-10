from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models.database import db
from datetime import datetime

#Import models (after db initialization to avoid circular imports)
from models.agency import Agency
from models.agent import Agent
from models.customer import Customer
from models.policy import Policy
from models.claim import Claim

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# Register blueprints
from routes.agency_routes import agency_bp
from routes.agent_routes import agent_bp
from routes.customer_routes import customer_bp
from routes.policy_routes import policy_bp
from routes.claim_routes import claim_bp

app.register_blueprint(agency_bp, url_prefix='/agencies')
app.register_blueprint(agent_bp, url_prefix='/agents')
app.register_blueprint(customer_bp, url_prefix='/customers')
app.register_blueprint(policy_bp, url_prefix='/policies')
app.register_blueprint(claim_bp, url_prefix='/claims')

# Add 'now' to the Jinja2 template context
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Home route
@app.route('/')
def index():

    # Dashboard summary data
    agency_count = Agency.query.count()
    agent_count = Agent.query.count()
    customer_count = Customer.query.count()
    policy_count = Policy.query.count()
    claim_count = Claim.query.count()
    
    # Get recent policies
    recent_policies = Policy.query.order_by(Policy.start_date.desc()).limit(4).all()
    
    # Get upcoming renewals
    upcoming_renewals = Policy.query.filter(
        Policy.end_date.isnot(None)
    ).order_by(Policy.end_date.asc()).limit(4).all()
    
    # Get recent claims
    recent_claims = Claim.query.order_by(Claim.claim_date.desc()).limit(4).all()
    
    # Get open claims
    open_claims = Claim.query.filter(
        Claim.status.in_(['Open', 'In Progress', 'Under Review'])
    ).order_by(Claim.claim_date.asc()).limit(4).all()
    
    return render_template('index.html', 
                           agency_count=agency_count,
                           agent_count=agent_count,
                           customer_count=customer_count,
                           policy_count=policy_count,
                           claim_count=claim_count,
                           recent_policies=recent_policies,
                           upcoming_renewals=upcoming_renewals,
                           recent_claims=recent_claims,
                           open_claims=open_claims)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('layout/error.html', error_code=404, 
                          error_message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('layout/error.html', error_code=500, 
                          error_message="Internal server error"), 500

# Command to create database tables
@app.cli.command("create-db")
def create_db_command():
    """Create database tables."""
    db.create_all()
    print("Database initialized!")

if __name__ == '__main__':
    app.run(debug=True)