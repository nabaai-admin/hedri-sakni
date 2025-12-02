from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Area(db.Model):
    """Area model for managing geographical areas"""
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    link = db.Column(db.String(500))  # Link to land location/details
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customers = db.relationship('Customer', back_populates='area', cascade='all, delete-orphan')
    reservation_slots = db.relationship('ReservationSlot', back_populates='area', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Customer(db.Model):
    """Customer model with Arabic field support"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # الاسم
    phone_number = db.Column(db.String(20), nullable=False)  # رقم الهاتف
    national_id = db.Column(db.String(50), nullable=False, unique=True)  # الرقم الوطني
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)  # المنطقة
    reservation_status = db.Column(
        db.String(20), 
        nullable=False, 
        default='OPEN'
    )  # حالة الحجز (OPEN, SUCCESS, FAILED)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    area = db.relationship('Area', back_populates='customers')
    reservation_attempts = db.relationship('ReservationAttempt', back_populates='customer', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'national_id': self.national_id,
            'area_id': self.area_id,
            'area_name': self.area.name if self.area else None,
            'reservation_status': self.reservation_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ReservationSlot(db.Model):
    """Reservation slots per area with scheduled date and time"""
    __tablename__ = 'reservation_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    scheduled_datetime = db.Column(db.DateTime, nullable=False)
    is_processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    area = db.relationship('Area', back_populates='reservation_slots')
    reservation_attempts = db.relationship('ReservationAttempt', back_populates='reservation_slot', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'area_id': self.area_id,
            'area_name': self.area.name if self.area else None,
            'scheduled_datetime': self.scheduled_datetime.isoformat() if self.scheduled_datetime else None,
            'is_processed': self.is_processed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ReservationAttempt(db.Model):
    """Tracks reservation attempts and responses from external API"""
    __tablename__ = 'reservation_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    reservation_slot_id = db.Column(db.Integer, db.ForeignKey('reservation_slots.id'), nullable=False)
    
    # Request data
    request_sent_at = db.Column(db.DateTime)
    request_payload = db.Column(db.JSON)
    
    # Response data
    response_received_at = db.Column(db.DateTime)
    response_status = db.Column(db.String(20))  # SUCCESS, FAILED
    response_code = db.Column(db.Integer)
    response_message = db.Column(db.Text)  # Stored exactly as received
    response_payload = db.Column(db.JSON)  # Full response for traceability
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer', back_populates='reservation_attempts')
    reservation_slot = db.relationship('ReservationSlot', back_populates='reservation_attempts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'customer_national_id': self.customer.national_id if self.customer else None,
            'reservation_slot_id': self.reservation_slot_id,
            'scheduled_datetime': self.reservation_slot.scheduled_datetime.isoformat() if self.reservation_slot and self.reservation_slot.scheduled_datetime else None,
            'area_name': self.reservation_slot.area.name if self.reservation_slot and self.reservation_slot.area else None,
            'request_sent_at': self.request_sent_at.isoformat() if self.request_sent_at else None,
            'request_payload': self.request_payload,
            'response_received_at': self.response_received_at.isoformat() if self.response_received_at else None,
            'response_status': self.response_status,
            'response_code': self.response_code,
            'response_message': self.response_message,
            'response_payload': self.response_payload,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
