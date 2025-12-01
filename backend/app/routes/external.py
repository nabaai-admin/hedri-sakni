from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from
from datetime import datetime
import logging

from app.models import db, Customer, ReservationAttempt
from app.schemas import ExternalUpdateSchema

logger = logging.getLogger(__name__)

external_bp = Blueprint('external', __name__, url_prefix='/api/external')
update_schema = ExternalUpdateSchema()


@external_bp.route('/update', methods=['POST'])
@swag_from({
    'tags': ['External Integration'],
    'summary': 'Update customer reservation status (called by UiPath)',
    'description': 'This endpoint is called by the external automation system to update reservation status',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['national_id', 'status', 'response_code', 'message'],
                'properties': {
                    'national_id': {
                        'type': 'string',
                        'description': 'Customer national ID'
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['SUCCESS', 'FAILED'],
                        'description': 'Reservation status'
                    },
                    'response_code': {
                        'type': 'integer',
                        'description': 'Response code from automation'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'Response message (stored exactly as received)'
                    },
                    'additional_data': {
                        'type': 'object',
                        'description': 'Any additional data from automation'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Status updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Validation error'},
        404: {'description': 'Customer not found'}
    }
})
def update_status():
    """
    External webhook endpoint for UiPath to update customer reservation status
    
    This endpoint:
    1. Receives status update from external automation
    2. Updates customer reservation status
    3. Records the response in reservation attempt
    4. Stores all data exactly as received for traceability
    """
    try:
        data = update_schema.load(request.json)
    except ValidationError as err:
        logger.error(f"Validation error in external update: {err.messages}")
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400
    
    national_id = data['national_id']
    status = data['status']
    response_code = data['response_code']
    message = data['message']
    additional_data = data.get('additional_data', {})
    
    logger.info(f"Received external update for national_id: {national_id}, status: {status}")
    
    # Find customer by national ID
    customer = Customer.query.filter_by(national_id=national_id).first()
    if not customer:
        logger.error(f"Customer not found with national_id: {national_id}")
        return jsonify({
            'success': False,
            'message': 'Customer not found'
        }), 404
    
    # Update customer status
    customer.reservation_status = status
    
    # Find the most recent reservation attempt for this customer
    attempt = ReservationAttempt.query.filter_by(
        customer_id=customer.id
    ).order_by(ReservationAttempt.created_at.desc()).first()
    
    if attempt:
        # Update the attempt with response data
        attempt.response_received_at = datetime.utcnow()
        attempt.response_status = status
        attempt.response_code = response_code
        attempt.response_message = message  # Stored exactly as received
        attempt.response_payload = {
            'status': status,
            'code': response_code,
            'message': message,
            'additional_data': additional_data,
            'timestamp': datetime.utcnow().isoformat()
        }
    else:
        logger.warning(f"No reservation attempt found for customer {customer.id}")
    
    db.session.commit()
    
    logger.info(f"Successfully updated status for customer {customer.id} to {status}")
    
    return jsonify({
        'success': True,
        'message': 'Status updated successfully',
        'customer_id': customer.id,
        'updated_status': status
    }), 200


@external_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['External Integration'],
    'summary': 'Health check endpoint',
    'responses': {
        200: {
            'description': 'Service is healthy',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'timestamp': {'type': 'string'}
                }
            }
        }
    }
})
def health_check():
    """Health check endpoint for external systems"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
