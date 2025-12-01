from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from

from app.models import db, Customer, Area
from app.schemas import CustomerSchema
from app.utils.auth import token_required

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@customers_bp.route('', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Customers'],
    'summary': 'Get all customers',
    'description': 'Retrieve a list of all customers with optional filtering',
    'parameters': [
        {
            'name': 'area_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter by area ID'
        },
        {
            'name': 'reservation_status',
            'in': 'query',
            'type': 'string',
            'enum': ['OPEN', 'SUCCESS', 'FAILED'],
            'required': False,
            'description': 'Filter by reservation status'
        }
    ],
    'responses': {
        200: {'description': 'List of customers'}
    }
})
def get_customers():
    """Get all customers with optional filtering"""
    query = Customer.query
    
    # Apply filters
    area_id = request.args.get('area_id', type=int)
    if area_id:
        query = query.filter_by(area_id=area_id)
    
    status = request.args.get('reservation_status')
    if status:
        query = query.filter_by(reservation_status=status)
    
    customers = query.order_by(Customer.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': customers_schema.dump(customers)
    }), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Customers'],
    'summary': 'Get customer by ID',
    'parameters': [
        {
            'name': 'customer_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Customer details'},
        404: {'description': 'Customer not found'}
    }
})
def get_customer(customer_id):
    """Get a specific customer"""
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({
        'success': True,
        'data': customer_schema.dump(customer)
    }), 200


@customers_bp.route('', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Customers'],
    'summary': 'Create new customer',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'phone_number', 'national_id', 'area_id'],
                'properties': {
                    'name': {'type': 'string', 'description': 'الاسم'},
                    'phone_number': {'type': 'string', 'description': 'رقم الهاتف'},
                    'national_id': {'type': 'string', 'description': 'الرقم الوطني'},
                    'area_id': {'type': 'integer', 'description': 'المنطقة'},
                    'reservation_status': {
                        'type': 'string',
                        'enum': ['OPEN', 'SUCCESS', 'FAILED'],
                        'default': 'OPEN',
                        'description': 'حالة الحجز'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Customer created successfully'},
        400: {'description': 'Validation error'},
        409: {'description': 'Customer with this national ID already exists'}
    }
})
def create_customer():
    """Create a new customer"""
    try:
        data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400
    
    # Verify area exists
    area = Area.query.get(data['area_id'])
    if not area:
        return jsonify({
            'success': False,
            'message': 'Area not found'
        }), 404
    
    # Check if customer with this national_id already exists
    existing = Customer.query.filter_by(national_id=data['national_id']).first()
    if existing:
        return jsonify({
            'success': False,
            'message': 'Customer with this national ID already exists'
        }), 409
    
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Customer created successfully',
        'data': customer_schema.dump(customer)
    }), 201


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Customers'],
    'summary': 'Update customer',
    'parameters': [
        {
            'name': 'customer_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'national_id': {'type': 'string'},
                    'area_id': {'type': 'integer'},
                    'reservation_status': {
                        'type': 'string',
                        'enum': ['OPEN', 'SUCCESS', 'FAILED']
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Customer updated successfully'},
        400: {'description': 'Validation error'},
        404: {'description': 'Customer not found'}
    }
})
def update_customer(customer_id):
    """Update an existing customer"""
    customer = Customer.query.get_or_404(customer_id)
    
    try:
        data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400
    
    # Verify area exists if being updated
    if 'area_id' in data:
        area = Area.query.get(data['area_id'])
        if not area:
            return jsonify({
                'success': False,
                'message': 'Area not found'
            }), 404
    
    # Check for national_id conflict
    if 'national_id' in data and data['national_id'] != customer.national_id:
        existing = Customer.query.filter_by(national_id=data['national_id']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Customer with this national ID already exists'
            }), 409
    
    for key, value in data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Customer updated successfully',
        'data': customer_schema.dump(customer)
    }), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Customers'],
    'summary': 'Delete customer',
    'parameters': [
        {
            'name': 'customer_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Customer deleted successfully'},
        404: {'description': 'Customer not found'}
    }
})
def delete_customer(customer_id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(customer_id)
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Customer deleted successfully'
    }), 200
