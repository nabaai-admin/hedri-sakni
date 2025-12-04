from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from

from app.models import db, Area
from app.schemas import AreaSchema
from app.utils.auth import token_required

areas_bp = Blueprint('areas', __name__, url_prefix='/api/areas')
area_schema = AreaSchema()
areas_schema = AreaSchema(many=True)


@areas_bp.route('', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Areas'],
    'security': [{'Bearer': []}],
    'summary': 'Get all areas',
    'description': 'Retrieve a list of all areas',
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
            'name': 'is_active',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'description': 'Filter by active status'
        }
    ],
    'responses': {
        200: {
            'description': 'List of areas',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Area'}
                    }
                }
            }
        }
    }
})
def get_areas():
    """Get all areas"""
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Area.query
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    areas = query.order_by(Area.name).all()
    return jsonify({
        'success': True,
        'data': areas_schema.dump(areas)
    }), 200


@areas_bp.route('/<int:area_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Areas'],
    'security': [{'Bearer': []}],
    'summary': 'Get area by ID',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (example: Bearer eyJhbGci...)'
        },
        {
            'name': 'area_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Area details'},
        404: {'description': 'Area not found'}
    }
})
def get_area(area_id):
    """Get a specific area"""
    area = Area.query.get_or_404(area_id)
    return jsonify({
        'success': True,
        'data': area_schema.dump(area)
    }), 200


@areas_bp.route('', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Areas'],
    'security': [{'Bearer': []}],
    'summary': 'Create new area',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (example: Bearer eyJhbGci...)'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name'],
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'link': {'type': 'string'},
                    'is_active': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Area created successfully'},
        400: {'description': 'Validation error'},
        409: {'description': 'Area already exists'}
    }
})
def create_area():
    """Create a new area"""
    try:
        data = area_schema.load(request.json)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400
    
    # Check if area already exists
    existing = Area.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({
            'success': False,
            'message': 'Area with this name already exists'
        }), 409
    
    area = Area(**data)
    db.session.add(area)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Area created successfully',
        'data': area_schema.dump(area)
    }), 201


@areas_bp.route('/<int:area_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Areas'],
    'security': [{'Bearer': []}],
    'summary': 'Update area',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (example: Bearer eyJhbGci...)'
        },
        {
            'name': 'area_id',
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
                    'description': {'type': 'string'},
                    'link': {'type': 'string'},
                    'is_active': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Area updated successfully'},
        400: {'description': 'Validation error'},
        404: {'description': 'Area not found'}
    }
})
def update_area(area_id):
    """Update an existing area"""
    area = Area.query.get_or_404(area_id)
    
    try:
        data = area_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400
    
    # Check for name conflict
    if 'name' in data and data['name'] != area.name:
        existing = Area.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Area with this name already exists'
            }), 409
    
    for key, value in data.items():
        setattr(area, key, value)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Area updated successfully',
        'data': area_schema.dump(area)
    }), 200


@areas_bp.route('/<int:area_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Areas'],
    'security': [{'Bearer': []}],
    'summary': 'Delete area',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (example: Bearer eyJhbGci...)'
        },
        {
            'name': 'area_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Area deleted successfully'},
        404: {'description': 'Area not found'}
    }
})
def delete_area(area_id):
    """Delete an area"""
    area = Area.query.get_or_404(area_id)
    
    db.session.delete(area)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Area deleted successfully'
    }), 200
