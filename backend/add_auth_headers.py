#!/usr/bin/env python3
"""Add Authorization header parameter to all Swagger endpoints"""

import re

# Authorization header template
AUTH_HEADER = """        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'default': 'Bearer YOUR_TOKEN_HERE',
            'description': 'MUST start with Bearer followed by space and token. Example: Bearer eyJhbGci...'
        },
"""

files_to_update = [
    '/home/abdulrasheed/NabaAI/hedri-sakni/backend/app/routes/reservations.py',
    '/home/abdulrasheed/NabaAI/hedri-sakni/backend/app/routes/analytics.py',
]

for filepath in files_to_update:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all @swag_from blocks with parameters
    # Add Authorization header if not already present
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this is a parameters line
        if "'parameters': [" in line and 'Authorization' not in content:
            # Look ahead to see if Authorization is already there
            next_param_line = i + 1
            if next_param_line < len(lines) and 'Authorization' not in lines[next_param_line]:
                # Add Authorization header
                new_lines.append(AUTH_HEADER.rstrip('\n'))
        
        i += 1
    
    # Write back
    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"Updated {filepath}")

print("Done!")
