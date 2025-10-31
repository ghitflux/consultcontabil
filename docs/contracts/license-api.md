# License API Contracts

## Overview

API endpoints for managing licenses, certifications, CNAEs, and municipal registrations.

Base URL: `/api/v1`

---

## Licenses

### GET /licenses

List licenses with filters and pagination.

**Query Parameters:**
- `client_id` (string, optional): Filter by client UUID
- `license_type` (string, optional): Filter by license type
- `status` (string, optional): Filter by status
- `search` (string, optional): Search in registration_number, issuing_authority
- `expiring_soon` (boolean, optional): Filter licenses expiring within 30 days
- `expired` (boolean, optional): Filter expired licenses
- `page` (integer, optional, default: 1): Page number
- `size` (integer, optional, default: 20): Items per page

**Response:** `LicenseListResponse`
```json
{
  "items": [
    {
      "id": "uuid",
      "client_id": "uuid",
      "license_type": "alvara_funcionamento",
      "registration_number": "ALV-2024-12345",
      "issuing_authority": "Prefeitura Municipal",
      "issue_date": "2024-01-15",
      "expiration_date": "2025-01-15",
      "status": "ativa",
      "document_id": "uuid",
      "notes": "Renovado em 2024",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z",
      "days_until_expiration": 45,
      "is_expired": false,
      "is_expiring_soon": false,
      "client_name": "Empresa Exemplo LTDA",
      "document_url": "/uploads/..."
    }
  ],
  "total": 50,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

**Authorization:** Admin, Employee, Client (client can only see own licenses)

---

### GET /licenses/:id

Get license details by ID.

**Response:** `LicenseResponse`

**Authorization:** Admin, Employee, Client (client can only see own licenses)

---

### POST /licenses

Create a new license.

**Request Body:** `LicenseCreate`
```json
{
  "client_id": "uuid",
  "license_type": "alvara_funcionamento",
  "registration_number": "ALV-2024-12345",
  "issuing_authority": "Prefeitura Municipal de São Paulo",
  "issue_date": "2024-01-15",
  "expiration_date": "2025-01-15",
  "notes": "Alvará de funcionamento para comércio varejista",
  "document_id": "uuid"
}
```

**Response:** `LicenseResponse` (201 Created)

**Authorization:** Admin, Employee only

---

### PUT /licenses/:id

Update an existing license.

**Request Body:** `LicenseUpdate`
```json
{
  "registration_number": "ALV-2024-67890",
  "expiration_date": "2025-12-31",
  "status": "ativa",
  "notes": "Número atualizado após renovação"
}
```

**Response:** `LicenseResponse`

**Authorization:** Admin, Employee only

---

### DELETE /licenses/:id

Delete a license (soft delete).

**Response:** 204 No Content

**Authorization:** Admin only

---

### POST /licenses/:id/renew

Renew a license.

**Request Body:** `LicenseRenewal`
```json
{
  "new_issue_date": "2025-01-15",
  "new_expiration_date": "2026-01-15",
  "new_registration_number": "ALV-2025-12345",
  "notes": "Renovação anual",
  "document_id": "uuid"
}
```

**Response:** `LicenseResponse` (new license)

**Note:** This marks the old license as expired and creates a new one.

**Authorization:** Admin, Employee only

---

### GET /licenses/:id/events

Get license event timeline.

**Response:** `LicenseEvent[]`
```json
[
  {
    "id": "uuid",
    "license_id": "uuid",
    "event_type": "created",
    "description": "Licença criada no sistema",
    "user_id": "uuid",
    "user_name": "João Silva",
    "created_at": "2024-01-15T10:00:00Z"
  },
  {
    "id": "uuid",
    "license_id": "uuid",
    "event_type": "renewed",
    "description": "Licença renovada por mais 1 ano",
    "user_id": "uuid",
    "user_name": "Maria Santos",
    "created_at": "2025-01-10T14:30:00Z"
  }
]
```

**Authorization:** Admin, Employee, Client (client can only see own license events)

---

### GET /licenses/statistics

Get license statistics for dashboard.

**Query Parameters:**
- `client_id` (string, optional): Filter stats by client

**Response:** `LicenseStatistics`
```json
{
  "total_licenses": 150,
  "active_licenses": 120,
  "expired_licenses": 15,
  "expiring_soon": 10,
  "pending_renewal": 5,
  "by_type": {
    "alvara_funcionamento": 50,
    "inscricao_municipal": 40,
    "certificado_digital": 30,
    "outros": 30
  },
  "by_status": {
    "ativa": 120,
    "vencida": 15,
    "pendente_renovacao": 10,
    "cancelada": 5
  }
}
```

**Authorization:** Admin, Employee, Client (client sees own stats)

---

### POST /licenses/check-expirations

Manually trigger expiration check and alerts.

**Response:**
```json
{
  "message": "Expiration check completed",
  "alerts_created": 5,
  "licenses_checked": 150
}
```

**Authorization:** Admin only

---

## CNAEs

### GET /cnaes

List CNAEs for a client.

**Query Parameters:**
- `client_id` (string, required): Client UUID
- `is_active` (boolean, optional): Filter by active status

**Response:** `CnaeListResponse`
```json
{
  "items": [
    {
      "id": "uuid",
      "client_id": "uuid",
      "cnae_code": "6201-5/00",
      "description": "Desenvolvimento de programas de computador sob encomenda",
      "cnae_type": "principal",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "client_name": "Empresa Exemplo LTDA"
    },
    {
      "id": "uuid",
      "client_id": "uuid",
      "cnae_code": "6202-3/00",
      "description": "Desenvolvimento e licenciamento de programas de computador customizáveis",
      "cnae_type": "secundario",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "client_name": "Empresa Exemplo LTDA"
    }
  ],
  "total": 3
}
```

**Authorization:** Admin, Employee, Client (client can only see own CNAEs)

---

### POST /cnaes

Create a new CNAE.

**Request Body:** `CnaeCreate`
```json
{
  "client_id": "uuid",
  "cnae_code": "6201-5/00",
  "description": "Desenvolvimento de programas de computador sob encomenda",
  "cnae_type": "principal"
}
```

**Response:** `CnaeResponse` (201 Created)

**Validation:**
- CNAE code must be in format `0000-0/00`
- Only one primary CNAE per client
- CNAE code must be unique per client

**Authorization:** Admin, Employee only

---

### PUT /cnaes/:id/set-primary

Set a CNAE as primary (removes primary status from others).

**Response:** `CnaeResponse`

**Note:** This automatically sets other CNAEs as secondary.

**Authorization:** Admin, Employee only

---

### DELETE /cnaes/:id

Delete a CNAE.

**Response:** 204 No Content

**Validation:**
- Cannot delete if it's the only CNAE
- If deleting primary CNAE, must set another as primary first

**Authorization:** Admin, Employee only

---

### POST /cnaes/validate

Validate CNAE code format.

**Request Body:**
```json
{
  "cnae_code": "620150"
}
```

**Response:** `CnaeValidation`
```json
{
  "is_valid": true,
  "cnae_code": "620150",
  "formatted_code": "6201-5/00",
  "error": null
}
```

**Authorization:** Admin, Employee

---

## Municipal Registrations

### GET /municipal-registrations

List municipal registrations with filters.

**Query Parameters:**
- `client_id` (string, optional): Filter by client UUID
- `state` (string, optional): Filter by state code (UF)
- `status` (string, optional): Filter by status
- `search` (string, optional): Search in city, registration_number
- `page` (integer, optional, default: 1): Page number
- `size` (integer, optional, default: 20): Items per page

**Response:** `MunicipalRegistrationListResponse`
```json
{
  "items": [
    {
      "id": "uuid",
      "client_id": "uuid",
      "city": "São Paulo",
      "state": "SP",
      "registration_number": "123.456.789-0",
      "issue_date": "2024-01-15",
      "status": "ativa",
      "notes": "Inscrição municipal - CCM",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z",
      "client_name": "Empresa Exemplo LTDA"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 20,
  "pages": 2
}
```

**Authorization:** Admin, Employee, Client (client can only see own registrations)

---

### GET /municipal-registrations/:id

Get municipal registration details by ID.

**Response:** `MunicipalRegistrationResponse`

**Authorization:** Admin, Employee, Client (client can only see own registrations)

---

### POST /municipal-registrations

Create a new municipal registration.

**Request Body:** `MunicipalRegistrationCreate`
```json
{
  "client_id": "uuid",
  "city": "São Paulo",
  "state": "SP",
  "registration_number": "123.456.789-0",
  "issue_date": "2024-01-15",
  "notes": "Inscrição Municipal - CCM para atividade de prestação de serviços"
}
```

**Response:** `MunicipalRegistrationResponse` (201 Created)

**Authorization:** Admin, Employee only

---

### PUT /municipal-registrations/:id

Update a municipal registration.

**Request Body:** `MunicipalRegistrationUpdate`
```json
{
  "registration_number": "987.654.321-0",
  "status": "ativa",
  "notes": "Número atualizado"
}
```

**Response:** `MunicipalRegistrationResponse`

**Authorization:** Admin, Employee only

---

### DELETE /municipal-registrations/:id

Delete a municipal registration (soft delete).

**Response:** 204 No Content

**Authorization:** Admin only

---

### GET /municipal-registrations/statistics

Get municipal registration statistics.

**Query Parameters:**
- `client_id` (string, optional): Filter stats by client

**Response:** `MunicipalRegistrationStatistics`
```json
{
  "total_registrations": 100,
  "active_registrations": 85,
  "inactive_registrations": 15,
  "by_state": {
    "SP": 50,
    "RJ": 30,
    "MG": 20
  },
  "by_status": {
    "ativa": 85,
    "inativa": 10,
    "suspensa": 5
  }
}
```

**Authorization:** Admin, Employee, Client (client sees own stats)

---

## Enums

### LicenseType
- `alvara_funcionamento` - Alvará de Funcionamento
- `inscricao_municipal` - Inscrição Municipal
- `inscricao_estadual` - Inscrição Estadual
- `certificado_digital` - Certificado Digital
- `licenca_ambiental` - Licença Ambiental
- `licenca_sanitaria` - Licença Sanitária
- `licenca_bombeiros` - Licença de Bombeiros
- `outros` - Outros

### LicenseStatus
- `ativa` - Ativa
- `vencida` - Vencida
- `pendente_renovacao` - Pendente Renovação
- `em_processo` - Em Processo
- `cancelada` - Cancelada
- `suspensa` - Suspensa

### LicenseEventType
- `created` - Criada
- `issued` - Emitida
- `renewed` - Renovada
- `expired` - Vencida
- `cancelled` - Cancelada
- `suspended` - Suspensa
- `reactivated` - Reativada
- `updated` - Atualizada
- `document_uploaded` - Documento Anexado

### CnaeType
- `principal` - Principal
- `secundario` - Secundário

### MunicipalRegistrationStatus
- `ativa` - Ativa
- `inativa` - Inativa
- `suspensa` - Suspensa
- `pendente` - Pendente
- `cancelada` - Cancelada

### StateCode
Standard Brazilian state codes (UF): AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO

---

## Business Rules

### Licenses
1. **Expiration Alerts**: Automatic alerts at 30, 15, 7, and 1 day before expiration
2. **Auto Status Update**: Status automatically changes to `vencida` when expiration_date passes
3. **Renewal**: Creates new license and marks old one as expired
4. **Document Attachment**: Optional but recommended for compliance

### CNAEs
1. **Format Validation**: Must be in format `0000-0/00` (e.g., `6201-5/00`)
2. **Primary Constraint**: Only one primary CNAE per client
3. **Uniqueness**: Same CNAE code cannot be added twice for the same client
4. **Minimum**: Client must have at least one CNAE

### Municipal Registrations
1. **State Validation**: Must use valid Brazilian state code
2. **Multiple Cities**: Client can have registrations in multiple cities
3. **Unique Number**: Registration number must be unique per city/state combination

---

## Error Responses

All endpoints follow standard error response format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "error_code": "VALIDATION_ERROR"
}
```

### Common Error Codes
- `VALIDATION_ERROR` (400): Invalid input data
- `NOT_FOUND` (404): Resource not found
- `UNAUTHORIZED` (401): Authentication required
- `FORBIDDEN` (403): Insufficient permissions
- `CONFLICT` (409): Resource conflict (e.g., duplicate CNAE)
- `UNPROCESSABLE_ENTITY` (422): Business rule violation

---

## WebSocket Events

License-related events broadcasted via WebSocket:

### license:expiring_soon
```json
{
  "type": "license:expiring_soon",
  "data": {
    "license_id": "uuid",
    "client_id": "uuid",
    "client_name": "Empresa Exemplo",
    "license_type": "alvara_funcionamento",
    "days_until_expiration": 7
  }
}
```

### license:expired
```json
{
  "type": "license:expired",
  "data": {
    "license_id": "uuid",
    "client_id": "uuid",
    "client_name": "Empresa Exemplo",
    "license_type": "certificado_digital"
  }
}
```

### license:renewed
```json
{
  "type": "license:renewed",
  "data": {
    "old_license_id": "uuid",
    "new_license_id": "uuid",
    "client_id": "uuid",
    "license_type": "inscricao_municipal"
  }
}
```
