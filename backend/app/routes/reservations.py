from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from
from datetime import datetime

from app.models import db, ReservationSlot, Area
from app.schemas import ReservationSlotSchema
from app.services.scheduler import reservation_scheduler
from app.utils.auth import token_required

reservations_bp = Blueprint('reservations', __name__, url_prefix='/api/reservations')
reservation_schema = ReservationSlotSchema()
reservations_schema = ReservationSlotSchema(many=True)


@reservations_bp.route('', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Reservation Slots'],
    'security': [{'Bearer': []}],
    'summary': 'Get all reservation slots',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'default': 'Bearer YOUR_TOKEN_HERE',
            'description': 'MUST start with Bearer followed by space and token. Example: Bearer eyJhbGci...'
        },
        {
            'name': 'area_id',
            'in': 'query',
            'type': 'integer',
            'required': False
        },
        {
            'name': 'is_processed',
            'in': 'query',
            'type': 'boolean',
            'required': False
        }
    ],
    'responses': {
        200: {
            'description': 'List of reservation slots',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/ReservationSlot'}
                    }
                }
            }
        }
    }
})
def get_reservation_slots():
    """Get all reservation slots with optional filtering"""
    query = ReservationSlot.query
    
    area_id = request.args.get('area_id', type=int)
    if area_id:
        query = query.filter_by(area_id=area_id)
    
    is_processed = request.args.get('is_processed', type=lambda v: v.lower() == 'true')
    if is_processed is not None:
        query = query.filter_by(is_processed=is_processed)
    
    slots = query.order_by(ReservationSlot.scheduled_datetime.desc()).all()
    return jsonify({
        'success': True,
        'data': reservations_schema.dump(slots)
    }), 200


@reservations_bp.route('/<int:slot_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Reservation Slots'],
    'security': [{'Bearer': []}],
    'summary': 'Get reservation slot by ID',
    'parameters': [
        {
            'name': 'slot_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Reservation slot details',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {'$ref': '#/definitions/ReservationSlot'}
                }
            }
        },
        404: {'description': 'Reservation slot not found'}
    }
})
def get_reservation_slot(slot_id):
    """Get a specific reservation slot"""
    slot = ReservationSlot.query.get_or_404(slot_id)
    return jsonify({
        'success': True,
        'data': reservation_schema.dump(slot)
    }), 200


@reservations_bp.route('', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Reservation Slots'],
    'security': [{'Bearer': []}],
    'summary': 'Create new reservation slot',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['area_id', 'scheduled_datetime'],
                'properties': {
                    'area_id': {'type': 'integer'},
                    'scheduled_datetime': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-12-15T10:00:00'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Reservation slot created and scheduled',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {'$ref': '#/definitions/ReservationSlot'}
                }
            }
        },
        400: {'description': 'Validation error'},
        404: {'description': 'Area not found'}
    }
})
def create_reservation_slot():
    """Create a new reservation slot and schedule it"""
    try:
        data = reservation_schema.load(request.json)
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
    
    # Validate scheduled datetime is in the future
    if data['scheduled_datetime'] <= datetime.utcnow():
        return jsonify({
            'success': False,
            'message': 'Scheduled datetime must be in the future'
        }), 400
    
    slot = ReservationSlot(**data)
    db.session.add(slot)
    db.session.commit()
    
    # Schedule the slot
    reservation_scheduler.schedule_reservation_slot(
        slot.id,
        slot.scheduled_datetime
    )
    
    return jsonify({
        'success': True,
        'message': 'Reservation slot created and scheduled successfully',
        'data': reservation_schema.dump(slot)
    }), 201


@reservations_bp.route('/<int:slot_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Reservation Slots'],
    'security': [{'Bearer': []}],
    'summary': 'Update reservation slot',
    'parameters': [
        {
            'name': 'slot_id',
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
                    'area_id': {'type': 'integer'},
                    'scheduled_datetime': {
                        'type': 'string',
                        'format': 'date-time'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Reservation slot updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {'$ref': '#/definitions/ReservationSlot'}
                }
            }
        },
        400: {'description': 'Validation error or slot already processed'},
        404: {'description': 'Reservation slot not found'}
    }
})
def update_reservation_slot(slot_id):
    """Update an existing reservation slot"""
    slot = ReservationSlot.query.get_or_404(slot_id)
    
    if slot.is_processed:
        return jsonify({
            'success': False,
            'message': 'Cannot update a processed reservation slot'
        }), 400
    
    try:
        data = reservation_schema.load(request.json, partial=True)
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
    
    # Validate scheduled datetime if being updated
    if 'scheduled_datetime' in data and data['scheduled_datetime'] <= datetime.utcnow():
        return jsonify({
            'success': False,
            'message': 'Scheduled datetime must be in the future'
        }), 400
    
    for key, value in data.items():
        setattr(slot, key, value)
    
    db.session.commit()
    
    # Reschedule if datetime changed
    if 'scheduled_datetime' in data:
        reservation_scheduler.schedule_reservation_slot(
            slot.id,
            slot.scheduled_datetime
        )
    
    return jsonify({
        'success': True,
        'message': 'Reservation slot updated successfully',
        'data': reservation_schema.dump(slot)
    }), 200


@reservations_bp.route('/<int:slot_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Reservation Slots'],
    'security': [{'Bearer': []}],
    'summary': 'Delete reservation slot',
    'parameters': [
        {
            'name': 'slot_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Reservation slot deleted'},
        400: {'description': 'Cannot delete processed slot'},
        404: {'description': 'Reservation slot not found'}
    }
})
def delete_reservation_slot(slot_id):
    """Delete a reservation slot"""
    slot = ReservationSlot.query.get_or_404(slot_id)
    
    if slot.is_processed:
        return jsonify({
            'success': False,
            'message': 'Cannot delete a processed reservation slot'
        }), 400
    
    # Remove from scheduler
    job_id = f"reservation_slot_{slot_id}"
    if reservation_scheduler.scheduler.get_job(job_id):
        reservation_scheduler.scheduler.remove_job(job_id)
    
    db.session.delete(slot)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Reservation slot deleted successfully'
    }), 200
