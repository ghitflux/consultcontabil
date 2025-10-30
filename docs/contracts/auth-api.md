# Authentication API Contracts

Documentação completa dos contratos de API para autenticação.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### 1. Login

Autentica um usuário e retorna tokens de acesso.

**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin",
    "is_active": true,
    "is_verified": true,
    "last_login_at": "2025-10-30T12:00:00Z",
    "created_at": "2025-10-30T10:00:00Z",
    "updated_at": "2025-10-30T12:00:00Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Credenciais inválidas
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```
- `422 Unprocessable Entity`: Dados de entrada inválidos

---

### 2. Refresh Token

Renova o access token usando o refresh token.

**Endpoint**: `POST /auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Responses**:
- `401 Unauthorized`: Token inválido ou expirado
  ```json
  {
    "detail": "Invalid or expired refresh token"
  }
  ```

---

### 3. Logout

Invalida os tokens do usuário (opcional).

**Endpoint**: `POST /auth/logout`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body** (optional):
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

---

### 4. Get Current User

Retorna informações do usuário autenticado.

**Endpoint**: `GET /users/me`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Admin User",
  "email": "admin@example.com",
  "role": "admin",
  "is_active": true,
  "is_verified": true,
  "last_login_at": "2025-10-30T12:00:00Z",
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T12:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Token inválido ou expirado

---

### 5. Create User

Cria um novo usuário (admin only).

**Endpoint**: `POST /users`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "name": "New User",
  "email": "user@example.com",
  "password": "password123",
  "role": "func"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "New User",
  "email": "user@example.com",
  "role": "func",
  "is_active": true,
  "is_verified": false,
  "last_login_at": null,
  "created_at": "2025-10-30T12:00:00Z",
  "updated_at": "2025-10-30T12:00:00Z"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `409 Conflict`: Email já existe
- `422 Unprocessable Entity`: Dados de entrada inválidos

---

### 6. Update User

Atualiza um usuário existente (admin ou próprio usuário).

**Endpoint**: `PUT /users/{user_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "name": "Updated Name",
  "email": "updated@example.com",
  "role": "admin",
  "is_active": true,
  "is_verified": true
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Updated Name",
  "email": "updated@example.com",
  "role": "admin",
  "is_active": true,
  "is_verified": true,
  "last_login_at": "2025-10-30T12:00:00Z",
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T13:00:00Z"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Usuário não encontrado
- `409 Conflict`: Email já existe

---

### 7. Update Password

Atualiza a senha do usuário autenticado.

**Endpoint**: `PUT /users/me/password`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password updated successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Senha atual incorreta
- `422 Unprocessable Entity`: Nova senha inválida

---

### 8. Request Password Reset

Solicita reset de senha (envia email com token).

**Endpoint**: `POST /auth/password-reset`

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

---

### 9. Confirm Password Reset

Confirma reset de senha com token.

**Endpoint**: `POST /auth/password-reset/confirm`

**Request Body**:
```json
{
  "token": "reset-token-here",
  "new_password": "newpassword123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Token inválido ou expirado

---

## Data Types

### UserRole Enum

```typescript
enum UserRole {
  ADMIN = "admin",     // Administrador do sistema
  FUNC = "func",       // Funcionário da contabilidade
  CLIENTE = "cliente"  // Cliente da contabilidade
}
```

### Token Specifications

- **Access Token**: JWT válido por 30 minutos
- **Refresh Token**: JWT válido por 7 dias
- **Token Type**: "bearer"
- **Algorithm**: HS256

### JWT Payload

```json
{
  "sub": "user-uuid",
  "role": "admin",
  "exp": 1698765432,
  "iat": 1698763632
}
```

---

## Error Handling

Todos os endpoints podem retornar os seguintes erros comuns:

- `500 Internal Server Error`: Erro interno do servidor
  ```json
  {
    "detail": "Internal server error"
  }
  ```

- `422 Unprocessable Entity`: Validação falhou
  ```json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ]
  }
  ```

---

## Security Notes

1. **HTTPS Only**: Em produção, todas as requisições devem usar HTTPS
2. **Token Storage**:
   - Access Token: Armazenar em memória (não em localStorage)
   - Refresh Token: Pode ser armazenado em localStorage ou httpOnly cookie
3. **Password Requirements**:
   - Mínimo 8 caracteres
   - Deve conter pelo menos uma letra e um número
4. **Rate Limiting**: Login endpoint limitado a 5 tentativas por minuto por IP
5. **CORS**: Configurado para aceitar apenas origens confiáveis

---

_Última atualização: 2025-10-30_
