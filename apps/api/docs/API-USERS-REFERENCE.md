# API Reference - Users & Client-User Management

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints require Bearer token authentication:
```
Authorization: Bearer {access_token}
```

---

## Endpoints

### 1. List Users
```http
GET /users
```

**Auth Required**: Admin only

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | No | Search by name or email |
| role | string | No | Filter by role (admin, func, cliente) |
| is_active | boolean | No | Filter by active status |
| page | integer | No | Page number (default: 1) |
| size | integer | No | Page size (default: 10) |

**Response**: `200 OK`
```json
{
  "items": [UserListItem],
  "total": 10,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

---

### 2. Create User
```http
POST /users
```

**Auth Required**: Admin only

**Request Body**:
```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "role": "admin" | "func" | "cliente"
}
```

**Response**: `201 Created` - UserResponse

---

### 3. Get User
```http
GET /users/{user_id}
```

**Auth Required**: Admin or Func

**Response**: `200 OK` - UserResponse

---

### 4. Update User
```http
PUT /users/{user_id}
```

**Auth Required**: Admin (full access) or Self (limited)

**Request Body**:
```json
{
  "name": "string",
  "email": "string",
  "role": "admin" | "func" | "cliente",
  "is_active": boolean,
  "is_verified": boolean
}
```

**Response**: `200 OK` - UserResponse

---

### 5. Activate User
```http
PATCH /users/{user_id}/activate
```

**Auth Required**: Admin only

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "User activated successfully"
}
```

---

### 6. Deactivate User
```http
PATCH /users/{user_id}/deactivate
```

**Auth Required**: Admin only

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "User deactivated successfully"
}
```

---

### 7. Reset User Password
```http
POST /users/{user_id}/reset-password
```

**Auth Required**: Admin only

**Request Body**:
```json
{
  "generate_temporary": true
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "temporary_password": "Xy3#jK8@pL2m",
  "message": "Password reset successfully"
}
```

---

### 8. Link User to Client
```http
POST /clients/{client_id}/users
```

**Auth Required**: Admin or Func

**Request Body**:
```json
{
  "user_id": "uuid",
  "access_level": "OWNER" | "MANAGER" | "VIEWER"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "message": "User linked to client successfully"
}
```

---

## Schemas

### UserResponse
```typescript
{
  id: string;
  name: string;
  email: string;
  role: "admin" | "func" | "cliente";
  is_active: boolean;
  is_verified: boolean;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
}
```

### UserListItem
```typescript
{
  id: string;
  name: string;
  email: string;
  role: "admin" | "func" | "cliente";
  is_active: boolean;
  is_verified: boolean;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid access level. Must be one of: OWNER, MANAGER, VIEWER"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to update this user"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 409 Conflict
```json
{
  "detail": "Email already registered"
}
```
