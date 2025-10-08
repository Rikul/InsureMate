from models.database import db
from datetime import datetime

class Claim(db.Model):
    __tablename__ = 'claim'
    
    claim_id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), nullable=False)
    claim_number = db.Column(db.String(50), nullable=False, unique=True)
    claim_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    incident_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    claim_amount = db.Column(db.DECIMAL(12, 2), default=0.00)
    status = db.Column(db.String(50), default='Open')
    resolution_date = db.Column(db.Date)
    settlement_amount = db.Column(db.DECIMAL(12, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Claim {self.claim_number}>'
    
    def is_open(self):
        """Check if the claim is currently open"""
        return self.status in ['Open', 'In Progress', 'Under Review']
    
    def is_closed(self):
        """Check if the claim is closed"""
        return self.status in ['Settled', 'Denied', 'Closed', 'Withdrawn']
    
    def days_since_filed(self):
        """Calculate days since claim was filed"""
        today = datetime.today().date()
        delta = today - self.claim_date
        return delta.days
    
    def to_dict(self):
        return {
            'claim_id': self.claim_id,
            'policy_id': self.policy_id,
            'claim_number': self.claim_number,
            'claim_date': self.claim_date.strftime('%Y-%m-%d') if self.claim_date else None,
            'incident_date': self.incident_date.strftime('%Y-%m-%d') if self.incident_date else None,
            'description': self.description,
            'claim_amount': float(self.claim_amount) if self.claim_amount else 0.0,
            'status': self.status,
            'resolution_date': self.resolution_date.strftime('%Y-%m-%d') if self.resolution_date else None,
            'settlement_amount': float(self.settlement_amount) if self.settlement_amount else 0.0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'days_since_filed': self.days_since_filed(),
            'is_open': self.is_open(),
            'policy_number': self.policy.policy_number if self.policy else None,
            'customer_name': self.policy.customer.full_name() if self.policy and self.policy.customer else None
        } 