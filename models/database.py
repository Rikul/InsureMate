from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database and migration with the Flask app."""

    from models.agency import Agency
    from models.agent import Agent
    from models.customer import Customer
    from models.policy import Policy
    from models.claim import Claim
    from sqlalchemy.exc import OperationalError

    db.init_app(app)
    migrate.init_app(app, db)
