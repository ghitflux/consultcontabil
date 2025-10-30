# Obligation API Contracts

Documentação completa dos contratos de API para gerenciamento de obrigações fiscais.

## Base URL

```
http://localhost:8000/api/v1
```

---

## Endpoints

### 1. List Obligations

Lista todas as obrigações com filtros e paginação.

**Endpoint**: `GET /obligations`

**Query Parameters**:
```
client_id: string (UUID, opcional) - Filtrar por cliente
status: string (opcional) - Filtrar por status (pendente, em_andamento, concluida, atrasada, cancelada)
priority: string (opcional) - Filtrar por prioridade (baixa, media, alta, urgente)
due_date_from: string (opcional) - Data de vencimento inicial (YYYY-MM-DD)
due_date_to: string (opcional) - Data de vencimento final (YYYY-MM-DD)
search: string (opcional) - Busca em descrição ou nome do tipo
page: number (opcional, default: 1) - Número da página
size: number (opcional, default: 10) - Itens por página
```

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "client_id": "123e4567-e89b-12d3-a456-426614174000",
      "client_name": "Comercial Silva e Filhos LTDA",
      "client_cnpj": "12.345.678/0001-90",
      "obligation_type_id": "789e0123-e45b-67c8-d901-234567890123",
      "obligation_type_name": "DAS - Documento de Arrecadação do Simples Nacional",
      "obligation_type_code": "DAS_MENSAL",
      "due_date": "2025-11-20",
      "status": "pendente",
      "priority": "media",
      "description": "Referência: 10/2025",
      "receipt_url": null,
      "completed_at": null,
      "completed_by_name": null,
      "created_at": "2025-10-30T10:00:00Z",
      "updated_at": null
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

**Permissions**: Admin, Func (todos), Cliente (apenas suas obrigações)

---

### 2. Get Obligation

Retorna detalhes completos de uma obrigação.

**Endpoint**: `GET /obligations/{obligation_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "client_id": "123e4567-e89b-12d3-a456-426614174000",
  "client_name": "Comercial Silva e Filhos LTDA",
  "client_cnpj": "12.345.678/0001-90",
  "obligation_type_id": "789e0123-e45b-67c8-d901-234567890123",
  "obligation_type_name": "DAS - Documento de Arrecadação do Simples Nacional",
  "obligation_type_code": "DAS_MENSAL",
  "due_date": "2025-11-20",
  "status": "pendente",
  "priority": "media",
  "description": "Referência: 10/2025",
  "receipt_url": null,
  "completed_at": null,
  "completed_by_name": null,
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- `404 Not Found`: Obrigação não encontrada
- `403 Forbidden`: Cliente tentando acessar obrigação de outro cliente

---

### 3. Create Obligation

Cria uma nova obrigação (admin ou func only).

**Endpoint**: `POST /obligations`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "client_id": "123e4567-e89b-12d3-a456-426614174000",
  "obligation_type_id": "789e0123-e45b-67c8-d901-234567890123",
  "due_date": "2025-11-20",
  "description": "Referência: 10/2025",
  "priority": "media"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "client_id": "123e4567-e89b-12d3-a456-426614174000",
  "client_name": "Comercial Silva e Filhos LTDA",
  "client_cnpj": "12.345.678/0001-90",
  "obligation_type_id": "789e0123-e45b-67c8-d901-234567890123",
  "obligation_type_name": "DAS - Documento de Arrecadação do Simples Nacional",
  "obligation_type_code": "DAS_MENSAL",
  "due_date": "2025-11-20",
  "status": "pendente",
  "priority": "media",
  "description": "Referência: 10/2025",
  "receipt_url": null,
  "completed_at": null,
  "completed_by_name": null,
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Cliente ou tipo de obrigação não encontrado
- `422 Unprocessable Entity`: Dados inválidos

---

### 4. Update Obligation

Atualiza uma obrigação existente (admin ou func only).

**Endpoint**: `PUT /obligations/{obligation_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "status": "em_andamento",
  "priority": "alta",
  "description": "Atualizado: Referência: 10/2025"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "em_andamento",
  "priority": "alta",
  ...
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Obrigação não encontrada

---

### 5. Delete Obligation

Remove uma obrigação (soft delete, admin only).

**Endpoint**: `DELETE /obligations/{obligation_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Obligation deleted successfully"
}
```

**Error Responses**:
- `403 Forbidden`: Apenas admin pode deletar
- `404 Not Found`: Obrigação não encontrada

---

### 6. Upload Receipt

Faz upload do comprovante e marca obrigação como concluída.

**Endpoint**: `POST /obligations/{obligation_id}/receipt`

**Headers**:
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body** (multipart/form-data):
```
file: File (required) - PDF, JPG, JPEG ou PNG
notes: string (optional) - Observações sobre o comprovante
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "concluida",
  "receipt_url": "/uploads/obligations/550e8400-e29b-41d4-a716-446655440000/comprovante.pdf",
  "completed_at": "2025-10-30T14:30:00Z",
  "completed_by_name": "João Silva",
  ...
}
```

**Error Responses**:
- `400 Bad Request`: Obrigação já concluída
- `400 Bad Request`: Tipo de arquivo não permitido
- `413 Payload Too Large`: Arquivo muito grande (máximo 10MB)
- `404 Not Found`: Obrigação não encontrada

---

### 7. Get Obligation Events

Retorna timeline de eventos de uma obrigação.

**Endpoint**: `GET /obligations/{obligation_id}/events`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
[
  {
    "id": "event-uuid-1",
    "obligation_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user-uuid",
    "user_name": "João Silva",
    "event_type": "completed",
    "description": "Obrigação concluída por João Silva",
    "metadata": {
      "notes": "Comprovante anexado"
    },
    "created_at": "2025-10-30T14:30:00Z"
  },
  {
    "id": "event-uuid-2",
    "obligation_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user-uuid",
    "user_name": "Maria Santos",
    "event_type": "started",
    "description": "Obrigação iniciada por Maria Santos",
    "metadata": null,
    "created_at": "2025-10-30T10:00:00Z"
  },
  {
    "id": "event-uuid-3",
    "obligation_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": null,
    "user_name": null,
    "event_type": "created",
    "description": "Obrigação criada automaticamente",
    "metadata": {
      "source": "monthly_generation"
    },
    "created_at": "2025-10-30T00:00:00Z"
  }
]
```

---

### 8. Generate Obligations

Gera obrigações para um mês de referência (admin only).

**Endpoint**: `POST /obligations/generate`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "reference_month": "2025-11-01",
  "client_ids": ["client-uuid-1", "client-uuid-2"]
}
```

**Response** (200 OK):
```json
{
  "reference_month": "2025-11-01",
  "total_created": 45,
  "total_clients": 6,
  "status": "success"
}
```

**Error Responses**:
- `403 Forbidden`: Apenas admin
- `400 Bad Request`: Obrigações já geradas para este mês

---

### 9. Get Statistics

Retorna estatísticas de obrigações.

**Endpoint**: `GET /obligations/statistics`

**Query Parameters**:
```
client_id: string (UUID, opcional) - Estatísticas de um cliente específico
date_from: string (opcional) - Data inicial
date_to: string (opcional) - Data final
```

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "total": 150,
  "by_status": {
    "pendente": 45,
    "em_andamento": 20,
    "concluida": 80,
    "atrasada": 5,
    "cancelada": 0
  },
  "by_priority": {
    "baixa": 30,
    "media": 60,
    "alta": 40,
    "urgente": 20
  },
  "overdue": 5,
  "due_this_week": 12,
  "due_this_month": 35,
  "completion_rate": 53.33
}
```

---

## Obligation Types Endpoints

### 10. List Obligation Types

**Endpoint**: `GET /obligation-types`

**Query Parameters**:
```
is_active: boolean (opcional) - Filtrar por ativos
page: number (opcional)
size: number (opcional)
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "789e0123-e45b-67c8-d901-234567890123",
      "name": "DAS - Documento de Arrecadação do Simples Nacional",
      "code": "DAS_MENSAL",
      "description": "Tributo mensal para empresas do Simples Nacional",
      "applies_to_commerce": true,
      "applies_to_service": true,
      "applies_to_industry": true,
      "applies_to_mei": false,
      "applies_to_simples": true,
      "applies_to_presumido": false,
      "applies_to_real": false,
      "recurrence": "mensal",
      "day_of_month": 20,
      "month_of_year": null,
      "is_active": true,
      "created_at": "2025-10-30T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 20,
  "page": 1,
  "size": 10,
  "pages": 2
}
```

---

## Data Types

### ObligationStatus Enum

```typescript
enum ObligationStatus {
  PENDENTE = "pendente",
  EM_ANDAMENTO = "em_andamento",
  CONCLUIDA = "concluida",
  ATRASADA = "atrasada",
  CANCELADA = "cancelada"
}
```

### ObligationPriority Enum

```typescript
enum ObligationPriority {
  BAIXA = "baixa",
  MEDIA = "media",
  ALTA = "alta",
  URGENTE = "urgente"
}
```

### ObligationRecurrence Enum

```typescript
enum ObligationRecurrence {
  MENSAL = "mensal",
  BIMESTRAL = "bimestral",
  TRIMESTRAL = "trimestral",
  SEMESTRAL = "semestral",
  ANUAL = "anual"
}
```

---

## Business Rules

### Status Transitions

- `PENDENTE` → `EM_ANDAMENTO` → `CONCLUIDA`
- `PENDENTE` → `ATRASADA` (automaticamente após vencimento)
- Qualquer status → `CANCELADA` (admin only)
- `CONCLUIDA` não pode ser revertida

### Priority Calculation

Prioridade é calculada automaticamente baseada em dias até vencimento:
- Vencida: `URGENTE`
- 1-3 dias: `ALTA`
- 4-7 dias: `MEDIA`
- 8+ dias: `BAIXA`

### Receipt Upload

- Arquivo obrigatório para marcar como concluída
- Extensões permitidas: `.pdf`, `.jpg`, `.jpeg`, `.png`
- Tamanho máximo: 10MB
- Armazenado em: `/var/uploads/obligations/{obligation_id}/`

### Generation Rules

- Obrigações são geradas para o próximo mês
- Baseado em tipo de empresa e regime tributário do cliente
- Não permite duplicatas para mesmo mês/cliente/tipo

---

## Permissions

| Endpoint | Admin | Func | Cliente |
|----------|-------|------|---------|
| GET /obligations | ✅ | ✅ | ✅ (próprias) |
| GET /obligations/:id | ✅ | ✅ | ✅ (próprias) |
| POST /obligations | ✅ | ✅ | ❌ |
| PUT /obligations/:id | ✅ | ✅ | ❌ |
| DELETE /obligations/:id | ✅ | ❌ | ❌ |
| POST /obligations/:id/receipt | ✅ | ✅ | ❌ |
| GET /obligations/:id/events | ✅ | ✅ | ✅ (próprias) |
| POST /obligations/generate | ✅ | ❌ | ❌ |
| GET /obligations/statistics | ✅ | ✅ | ✅ (próprias) |
| GET /obligation-types | ✅ | ✅ | ❌ |

---

_Última atualização: 2025-10-30_
