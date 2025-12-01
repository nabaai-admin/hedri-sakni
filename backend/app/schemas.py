from marshmallow import Schema, fields, validate


class AreaSchema(Schema):
    """Schema for Area validation and serialization"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CustomerSchema(Schema):
    """Schema for Customer validation and serialization"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    phone_number = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    national_id = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    area_id = fields.Int(required=True)
    area_name = fields.Str(dump_only=True)
    reservation_status = fields.Str(
        validate=validate.OneOf(['OPEN', 'SUCCESS', 'FAILED']),
        load_default='OPEN'
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ReservationSlotSchema(Schema):
    """Schema for ReservationSlot validation and serialization"""
    id = fields.Int(dump_only=True)
    area_id = fields.Int(required=True)
    area_name = fields.Str(dump_only=True)
    scheduled_datetime = fields.DateTime(required=True)
    is_processed = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ReservationAttemptSchema(Schema):
    """Schema for ReservationAttempt validation and serialization"""
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    customer_name = fields.Str(dump_only=True)
    customer_national_id = fields.Str(dump_only=True)
    reservation_slot_id = fields.Int(required=True)
    scheduled_datetime = fields.DateTime(dump_only=True)
    area_name = fields.Str(dump_only=True)
    request_sent_at = fields.DateTime(dump_only=True)
    request_payload = fields.Dict(dump_only=True)
    response_received_at = fields.DateTime(dump_only=True)
    response_status = fields.Str(dump_only=True)
    response_code = fields.Int(dump_only=True)
    response_message = fields.Str(dump_only=True)
    response_payload = fields.Dict(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ExternalUpdateSchema(Schema):
    """Schema for external API update webhook"""
    national_id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['SUCCESS', 'FAILED']))
    response_code = fields.Int(required=True)
    message = fields.Str(required=True)
    additional_data = fields.Dict(allow_none=True)


class LoginSchema(Schema):
    """Schema for admin login"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class AnalyticsFilterSchema(Schema):
    """Schema for analytics filtering"""
    area_id = fields.Int(allow_none=True)
    status = fields.Str(
        allow_none=True,
        validate=validate.OneOf(['OPEN', 'SUCCESS', 'FAILED'])
    )
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
