from models.database import db
from datetime import datetime, timedelta

class Policy(db.Model):
    __tablename__ = 'policy'
    
    policy_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.agent_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    policy_number = db.Column(db.String(50), nullable=False, unique=True)
    policy_type = db.Column(db.String(100), nullable=False)
    coverage_amount = db.Column(db.DECIMAL(12, 2), default=0.00)
    premium = db.Column(db.DECIMAL(10, 2), default=0.00)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    policy_status = db.Column(db.String(50), default='Active')
    
    # Relationships
    claims = db.relationship('Claim', backref='policy', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Policy {self.policy_number}>'
    
    def is_active(self):
        """Check if the policy is currently active"""
        today = datetime.today().date()
        return (
            self.policy_status == 'Active' and
            self.start_date <= today and
            (self.end_date is None or self.end_date >= today)
        )
    
    def days_until_renewal(self):
        """Calculate days until renewal"""
        if not self.end_date:
            return None
        today = datetime.today().date()
        delta = self.end_date - today
        return delta.days
    
    def renewal_status(self):
        """Return a status indicating renewal urgency"""
        if not self.end_date:
            return None
            
        days = self.days_until_renewal()
        
        if days < 0:
            return "Expired"
        elif days <= 7:
            return "Critical"
        elif days <= 30:
            return "Warning"
        else:
            return "OK"
    
    def to_dict(self):
        return {
            'policy_id': self.policy_id,
            'agent_id': self.agent_id,
            'customer_id': self.customer_id,
            'policy_number': self.policy_number,
            'policy_type': self.policy_type,
            'coverage_amount': float(self.coverage_amount) if self.coverage_amount else 0.0,
            'premium': float(self.premium) if self.premium else 0.0,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'policy_status': self.policy_status,
            'is_active': self.is_active(),
            'days_until_renewal': self.days_until_renewal(),
            'renewal_status': self.renewal_status(),
            'agent_name': self.agent.full_name() if self.agent else None,
            'customer_name': self.customer.full_name() if self.customer else None,
            'claim_count': len(self.claims) if hasattr(self, 'claims') else 0
        }