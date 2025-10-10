from models.database import db
from sqlalchemy.orm import relationship

class Agent(db.Model):
    __tablename__ = 'agent'
    
    agent_id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.agency_id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    
    # Relationships
    policies = db.relationship('Policy', backref='agent', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Agent {self.first_name} {self.last_name}>'
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'agent_id': self.agent_id,
            'agency_id': self.agency_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'full_name': self.full_name(),
            'agency_name': self.agency.name if self.agency else None,
            'policy_count': len(self.policies) if self.policies else 0
        }