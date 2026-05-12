# Orethan Microfinance Mobile App API Documentation

## Base URL
```
http://127.0.0.1:5000/api
```

## Authentication

### Login
**POST** `/api/login` 
```json
{
    "username": "client_username",
    "password": "password"
}
```

**Response:**
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "Test Client",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "0712345678",
        "role": "client"
    }
}
```

### Register
**POST** `/api/register` 
```json
{
    "username": "new_user",
    "password": "password123",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "0712345678"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Registration successful",
    "user_id": 2
}
```

## Loan APIs (Requires Auth Token)

### Get My Loans
**GET** `/api/my_loans` 
*Header: Authorization: Bearer <token>*

**Response:**
```json
{
    "success": true,
    "loans": [
        {
            "id": 1,
            "amount": 1000000,
            "amount_formatted": "Tsh 1,000,000.00",
            "purpose": "Business",
            "status": "pending",
            "current_stage": "loan_officer",
            "stage_name": "Loan Officer Review",
            "term_months": 12,
            "monthly_payment": 83333.33,
            "monthly_payment_formatted": "Tsh 83,333.33",
            "created_at": "2024-01-15 10:30:00"
        }
    ]
}
```

### Apply for Loan
**POST** `/api/apply_loan` 
```json
{
    "amount": 1000000,
    "purpose": "Business",
    "term_months": 12
}
```

**Response:**
```json
{
    "success": true,
    "message": "Loan application submitted",
    "loan_id": 3
}
```

### Get Loan Status
**GET** `/api/loan_status/{loan_id}` 

**Response:**
```json
{
    "success": true,
    "loan": {
        "id": 1,
        "amount": 1000000,
        "amount_formatted": "Tsh 1,000,000.00",
        "purpose": "Business",
        "status": "pending",
        "current_stage": "loan_officer",
        "term_months": 12,
        "monthly_payment": 83333.33,
        "created_at": "2024-01-15 10:30:00",
        "approvals": []
    }
}
```

### Get Repayment Schedule
**GET** `/api/repayment_schedule/{loan_id}` 

**Response:**
```json
{
    "success": true,
    "loan": {
        "id": 1,
        "amount": 1000000,
        "monthly_payment": 83333.33,
        "term_months": 12
    },
    "schedule": [
        {
            "id": 1,
            "due_date": "2024-02-15",
            "amount_due": 83333.33,
            "amount_due_formatted": "Tsh 83,333.33",
            "amount_paid": 0,
            "status": "pending",
            "late_fee": 0,
            "payment_date": null
        }
    ],
    "summary": {
        "total_due": 1000000,
        "total_paid": 0,
        "remaining_balance": 1000000,
        "payments_made": 0
    }
}
```

## Payment APIs

### Make Payment
**POST** `/api/make_payment` 
```json
{
    "loan_id": 1,
    "amount": 100000,
    "phone_number": "0712345678"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Payment initiated. Check your phone to complete.",
    "checkout_request_id": "ws_CO_123456789"
}
```

### Payment History
**GET** `/api/payment_history` 

**Response:**
```json
{
    "success": true,
    "payments": [
        {
            "id": 1,
            "loan_id": 1,
            "amount": 100000,
            "amount_formatted": "Tsh 100,000.00",
            "method": "M-Pesa",
            "status": "completed",
            "transaction_id": "MPESA123456",
            "date": "2024-01-15 14:30:00"
        }
    ]
}
```

## Profile APIs

### Get Profile
**GET** `/api/profile` 

**Response:**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "Test Client",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "0712345678",
        "role": "client",
        "joined_date": "2024-01-01"
    }
}
```

### Update Profile
**PUT** `/api/update_profile` 
```json
{
    "full_name": "Updated Name",
    "email": "new@email.com",
    "phone": "0712345679"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Profile updated"
}
```

## Staff APIs

### Pending Approvals
**GET** `/api/pending_approvals` 

**Response:**
```json
{
    "success": true,
    "pending_approvals": [
        {
            "id": 1,
            "client_name": "John Doe",
            "amount": 1000000,
            "amount_formatted": "Tsh 1,000,000.00",
            "purpose": "Business",
            "term_months": 12,
            "created_at": "2024-01-15"
        }
    ]
}
```

### Approve Loan
**POST** `/api/approve_loan/{loan_id}` 

**Response:**
```json
{
    "success": true,
    "message": "Loan approved",
    "new_stage": "loan_manager"
}
```

### Reject Loan
**POST** `/api/reject_loan/{loan_id}` 

**Response:**
```json
{
    "success": true,
    "message": "Loan rejected/sent back"
}
```

## Dashboard Stats
**GET** `/api/dashboard_stats` 

**Client Response:**
```json
{
    "success": true,
    "stats": {
        "total_loans": 3,
        "active_loans": 1,
        "completed_loans": 1,
        "pending_loans": 1
    }
}
```

**Staff Response:**
```json
{
    "success": true,
    "stats": {
        "total_clients": 50,
        "total_loans": 100,
        "pending_approvals": 5
    }
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
    "success": false,
    "message": "Error description"
}
```

Common HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Mobile App Integration

### Flutter Example:
```dart
// Login
final response = await http.post(
  Uri.parse('http://127.0.0.1:5000/api/login'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'username': 'Test Client',
    'password': 'client123'
  }),
);

if (response.statusCode == 200) {
  final data = jsonDecode(response.body);
  final token = data['token'];
  // Store token for future requests
}
```

### React Native Example:
```javascript
// Get My Loans
const response = await fetch('http://127.0.0.1:5000/api/my_loans', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
```

## Security Notes

- All endpoints (except login/register) require JWT token
- Token expires in 30 days
- Use HTTPS in production
- Validate all input data
- Handle errors gracefully

## Testing

Use Postman or curl to test endpoints:

```bash
# Test Login
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Test Client","password":"client123"}'
```
