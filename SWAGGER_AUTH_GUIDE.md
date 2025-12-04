# SWAGGER UI AUTHENTICATION GUIDE

## The Issue You Were Experiencing
The Swagger UI was generating curl commands WITHOUT the Authorization header, causing 401 errors.

## Root Cause
Flasgger requires EXPLICIT `security: [{'Bearer': []}]` tags on each endpoint's Swagger definition to tell the UI to include the Authorization header in requests.

## What Was Fixed
✅ Added `security: [{'Bearer': []}]` to ALL protected endpoints (Areas, Customers, Reservations, Analytics)
✅ Added `security: []` to the login endpoint (to explicitly mark it as NOT requiring auth)
✅ Kept global security definition in swagger_template
✅ Backend restarted with correct configuration

## HOW TO USE SWAGGER UI - STEP BY STEP

### Step 1: Go to Swagger UI
Open: `https://hedri-apis.socialaipilot.com/api/docs`

### Step 2: Login to Get Token
1. Find the **Authentication** section
2. Expand `POST /api/auth/login`
3. Click **"Try it out"**
4. Replace the example JSON with:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
5. Click **Execute**
6. Copy the token from the response (it looks like `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

### Step 3: Authorize
1. Look at the TOP RIGHT of the Swagger UI page
2. Click the green **"Authorize"** button (🔓 icon)
3. A popup will appear with a field labeled "Value"
4. Enter: `Bearer <your_token_here>` (include the word "Bearer" followed by a space and your token)
   - Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzMzMzI3NjI1LCJpYXQiOjE3MzMzMjQwMjV9.abc123...`
5. Click **"Authorize"**
6. Click **"Close"**

### Step 4: Test Protected Endpoints
Now when you try any endpoint (like GET /api/areas):
1. The lock icon (🔒) should be CLOSED/LOCKED
2. Click "Try it out"
3. Click "Execute"
4. The generated curl command should NOW include:
```bash
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## VERIFICATION

### ✅ Correct curl command (with auth):
```bash
curl -X GET "https://hedri-apis.socialaipilot.com/api/areas" \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### ❌ Incorrect curl command (without auth):
```bash
curl -X GET "https://hedri-apis.socialaipilot.com/api/areas" \
  -H "accept: application/json"
```

## VISUAL INDICATORS IN SWAGGER UI

### Before Authorization:
- 🔓 Open lock icon next to "Authorize" button
- 🔒 Lock icon on each protected endpoint is OPEN

### After Authorization:
- 🔒 Closed lock icon next to "Authorize" button
- 🔒 Lock icon on each protected endpoint is CLOSED

## Common Mistakes

### ❌ WRONG: Just pasting the token
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ✅ CORRECT: "Bearer " + token
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ❌ WRONG: Using example values
```json
{
  "username": "string",
  "password": "string"
}
```

### ✅ CORRECT: Using actual credentials
```json
{
  "username": "admin",
  "password": "admin123"
}
```

## Token Expiration
- Tokens expire after 1 hour (3600 seconds)
- If you get a 401 error after using the API for a while, login again to get a new token
- Then re-authorize with the new token

## Technical Details

### What Changed in Code:
1. **backend/app/__init__.py**: Added `security: []` to login endpoint
2. **backend/app/routes/areas.py**: Added `security: [{'Bearer': []}]` to all 5 endpoints
3. **backend/app/routes/customers.py**: Added `security: [{'Bearer': []}]` to all 5 endpoints
4. **backend/app/routes/reservations.py**: Added `security: [{'Bearer': []}]` to all 5 endpoints
5. **backend/app/routes/analytics.py**: Added `security: [{'Bearer': []}]` to all 3 endpoints

### Why This Works:
- The `@token_required` decorator on the Python functions provides actual security
- The `security: [{'Bearer': []}]` in Swagger definitions tells the UI to send the header
- Both are needed: one for backend security, one for UI behavior

## Test Script
Run this to verify all endpoints work:
```bash
cd /home/abdulrasheed/NabaAI/hedri-sakni/backend
python3 test_all_apis.py
```

Expected output:
```
Total tests: 19
Passed: 19 (100.0%)
Failed: 0 (0.0%)
```
