from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from
from sqlalchemy import func, case
from datetime import datetime

from app.models import db, ReservationAttempt, Customer, Area, ReservationSlot
from app.schemas import AnalyticsFilterSchema, ReservationAttemptSchema
from app.utils.auth import token_required

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')
attempt_schema = ReservationAttemptSchema()
attempts_schema = ReservationAttemptSchema(many=True)


@analytics_bp.route('/summary', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Analytics'],
    'security': [{'Bearer': []}],
    'summary': 'Get aggregated reservation statistics',
    'parameters': [
        {
            'name': 'area_id',
            'in': 'query',
            'type': 'integer',
            'required': False
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False
        }
    ],
    'responses': {
        200: {
            'description': 'Aggregated statistics',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'total_attempts': {'type': 'integer'},
                            'success_count': {'type': 'integer'},
                            'failed_count': {'type': 'integer'},
                            'open_count': {'type': 'integer'},
                            'success_rate': {'type': 'number'},
                            'by_area': {'type': 'array'}
                        }
                    }
                }
            }
        }
    }
})
def get_summary():
    """Get aggregated reservation statistics"""
    # Parse filters
    area_id = request.args.get('area_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build base query for customers
    customer_query = db.session.query(
        Customer.reservation_status,
        func.count(Customer.id).label('count')
    )
    
    if area_id:
        customer_query = customer_query.filter(Customer.area_id == area_id)
    
    # Apply date filters through reservation attempts
    if start_date or end_date:
        customer_query = customer_query.join(ReservationAttempt)
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            customer_query = customer_query.filter(ReservationAttempt.created_at >= start_dt)
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            customer_query = customer_query.filter(ReservationAttempt.created_at <= end_dt)
    
    status_counts = customer_query.group_by(Customer.reservation_status).all()
    
    # Calculate totals
    total_attempts = sum(count for _, count in status_counts)
    success_count = next((count for status, count in status_counts if status == 'SUCCESS'), 0)
    failed_count = next((count for status, count in status_counts if status == 'FAILED'), 0)
    open_count = next((count for status, count in status_counts if status == 'OPEN'), 0)
    
    success_rate = (success_count / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get statistics by area
    area_query = db.session.query(
        Area.id,
        Area.name,
        func.count(Customer.id).label('total'),
        func.sum(case((Customer.reservation_status == 'SUCCESS', 1), else_=0)).label('success'),
        func.sum(case((Customer.reservation_status == 'FAILED', 1), else_=0)).label('failed'),
        func.sum(case((Customer.reservation_status == 'OPEN', 1), else_=0)).label('open')
    ).join(Customer, Area.id == Customer.area_id, isouter=True)
    
    if area_id:
        area_query = area_query.filter(Area.id == area_id)
    
    if start_date or end_date:
        area_query = area_query.join(ReservationAttempt, Customer.id == ReservationAttempt.customer_id, isouter=True)
        if start_date:
            area_query = area_query.filter(ReservationAttempt.created_at >= start_dt)
        if end_date:
            area_query = area_query.filter(ReservationAttempt.created_at <= end_dt)
    
    area_stats = area_query.group_by(Area.id, Area.name).all()
    
    by_area = []
    for area_id, area_name, total, success, failed, open_status in area_stats:
        total = total or 0
        success = success or 0
        failed = failed or 0
        open_status = open_status or 0
        
        by_area.append({
            'area_id': area_id,
            'area_name': area_name,
            'total': total,
            'success': success,
            'failed': failed,
            'open': open_status,
            'success_rate': (success / total * 100) if total > 0 else 0
        })
    
    return jsonify({
        'success': True,
        'data': {
            'total_attempts': total_attempts,
            'success_count': success_count,
            'failed_count': failed_count,
            'open_count': open_count,
            'success_rate': round(success_rate, 2),
            'by_area': by_area
        }
    }), 200


@analytics_bp.route('/attempts', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Analytics'],
    'security': [{'Bearer': []}],
    'summary': 'Get detailed reservation attempts',
    'parameters': [
        {
            'name': 'area_id',
            'in': 'query',
            'type': 'integer',
            'required': False
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['SUCCESS', 'FAILED'],
            'required': False
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False
        }
    ],
    'responses': {
        200: {
            'description': 'List of reservation attempts',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/ReservationAttempt'}
                    }
                }
            }
        }
    }
})
def get_attempts():
    """Get detailed reservation attempts with filtering"""
    query = ReservationAttempt.query.join(Customer).join(ReservationSlot).join(Area)
    
    # Apply filters
    area_id = request.args.get('area_id', type=int)
    if area_id:
        query = query.filter(Area.id == area_id)
    
    status = request.args.get('status')
    if status:
        query = query.filter(ReservationAttempt.response_status == status)
    
    start_date = request.args.get('start_date')
    if start_date:
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        query = query.filter(ReservationAttempt.created_at >= start_dt)
    
    end_date = request.args.get('end_date')
    if end_date:
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        query = query.filter(ReservationAttempt.created_at <= end_dt)
    
    attempts = query.order_by(ReservationAttempt.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': attempts_schema.dump(attempts)
    }), 200


@analytics_bp.route('/attempts/<int:attempt_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Analytics'],
    'security': [{'Bearer': []}],
    'summary': 'Get detailed reservation attempt by ID',
    'parameters': [
        {
            'name': 'attempt_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Reservation attempt details',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {'$ref': '#/definitions/ReservationAttempt'}
                }
            }
        },
        404: {'description': 'Attempt not found'}
    }
})
def get_attempt(attempt_id):
    """Get a specific reservation attempt"""
    attempt = ReservationAttempt.query.get_or_404(attempt_id)
    return jsonify({
        'success': True,
        'data': attempt_schema.dump(attempt)
    }), 200
