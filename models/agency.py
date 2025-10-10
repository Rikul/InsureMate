from models.database import db

class Agency(db.Model):
    __tablename__ = 'agency'
    
    agency_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Relationships
    agents = db.relationship('Agent', backref='agency', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Agency {self.name}>'
    
    def to_dict(self):
        return {
            'agency_id': self.agency_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'agent_count': len(self.agents) if self.agents else 0
        }