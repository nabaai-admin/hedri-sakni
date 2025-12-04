# Reservations and Analytics - Add Authorization Headers

## Files that still need Authorization headers:
1. `/home/abdulrasheed/NabaAI/hedri-sakni/backend/app/routes/reservations.py` - 5 endpoints
2. `/home/abdulrasheed/NabaAI/hedri-sakni/backend/app/routes/analytics.py` - 3 endpoints

## Authorization Header Template:
```python
{
    'name': 'Authorization',
    'in': 'header',
    'type': 'string',
    'required': True,
    'default': 'Bearer YOUR_TOKEN_HERE',
    'description': 'MUST start with Bearer followed by space and token. Example: Bearer eyJhbGci...'
},
```

Add this as the FIRST parameter in the `'parameters': [...]` list for each @swag_from decorator.

External.py endpoints (/external/update and /external/health) do NOT need authentication - they are for UiPath webhooks.
