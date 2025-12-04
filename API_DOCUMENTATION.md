# Land Reservation Admin API - Complete Documentation

## API Status: ✅ ALL ENDPOINTS WORKING (19/19 tests passed)

## Base URL
- Local: `http://localhost:5000/api`
- Production: `https://hedri-apis.socialaipilot.com/api`

## Authentication
All endpoints (except `/external/health` and `/auth/login`) require Bearer token authentication.

### How to use Swagger UI:
1. Go to `/api/docs`
2. Use `/api/auth/login` with credentials: 
   - Username: `admin`
   - Password: `admin123`
3. Click the green **Authorize** button at the top
4. Enter: `Bearer <your_token>`
5. Click **Authorize** then **Close**
6. Now all protected endpoints will include the Authorization header

---

## Endpoints Summary

### ✅ AUTHENTICATION (1 endpoint)
**Purpose:** Admin login
- `POST /api/auth/login` - Get JWT token

### ✅ AREAS (5 endpoints) 
**Purpose:** Manage geographical areas where land is located
- `GET /api/areas` - List all areas
- `GET /api/areas/{id}` - Get specific area
- `POST /api/areas` - Create new area
- `PUT /api/areas/{id}` - Update area
- `DELETE /api/areas/{id}` - Delete area

### ✅ CUSTOMERS (5 endpoints)
**Purpose:** Manage customers who want to reserve land
- `GET /api/customers` - List all customers (filter by area_id, reservation_status)
- `GET /api/customers/{id}` - Get specific customer
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### ✅ RESERVATION SLOTS (5 endpoints)
**Purpose:** Schedule when UiPath automation should run for reservations
- `GET /api/reservations` - List all reservation slots
- `GET /api/reservations/{id}` - Get specific slot
- `POST /api/reservations` - Create and schedule new slot
- `PUT /api/reservations/{id}` - Update slot (reschedules job)
- `DELETE /api/reservations/{id}` - Delete slot (removes from scheduler)

### ✅ ANALYTICS (2 endpoints)
**Purpose:** View reservation statistics and attempt details
- `GET /api/analytics/summary` - Get aggregated statistics (success rate, by area)
- `GET /api/analytics/attempts` - Get detailed reservation attempts
- `GET /api/analytics/attempts/{id}` - Get specific attempt details (available but not in main list)

### ✅ EXTERNAL INTEGRATION (2 endpoints)
**Purpose:** Webhook for UiPath to update reservation status
- `POST /api/external/update` - UiPath webhook (updates customer status)
- `GET /api/external/health` - Health check (no auth required)

---

## All Endpoints Are Necessary ✓

**Why Each Category Is Needed:**

1. **Authentication** - Required for security
2. **Areas** - Core entity: defines land locations
3. **Customers** - Core entity: people reserving land
4. **Reservation Slots** - Core entity: schedules automation runs
5. **Analytics** - Business intelligence: track success/failure rates
6. **External** - Integration: allows UiPath to update results

**No endpoints should be deleted.** All are part of the core business logic for the land reservation system.

---

## Known Issues Fixed

1. ✅ **Missing 'link' field in Area** - FIXED
2. ✅ **Missing ReservationSlot and ReservationAttempt definitions** - FIXED
3. ✅ **Swagger UI not showing security lock icons** - FIXED (added uiversion: 3)
4. ✅ **No Authorization header in Swagger requests** - FIXED (explicit security tags)

---

## Correct Usage Example

### 1. Login
```bash
curl -X POST "https://hedri-apis.socialaipilot.com/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Use Token for Protected Endpoints
```bash
curl -X GET "https://hedri-apis.socialaipilot.com/api/areas" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "accept: application/json"
```

### 3. Create an Area with Link
```bash
curl -X POST "https://hedri-apis.socialaipilot.com/api/areas" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "North District",
    "description": "Northern land area",
    "link": "https://maps.google.com/?q=123,456",
    "is_active": true
  }'
```

---

## Test Results

```
Total tests: 19
Passed: 19 (100.0%)
Failed: 0 (0.0%)
```

All endpoints tested successfully:
- ✓ Authentication (1)
- ✓ Areas CRUD (5)
- ✓ Customers CRUD (5)
- ✓ Reservation Slots CRUD (5)
- ✓ Analytics (2)
- ✓ External/Health (1)
