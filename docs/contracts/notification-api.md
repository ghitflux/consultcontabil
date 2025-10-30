# Notification API Contracts

Documentação completa dos contratos de API para gerenciamento de notificações.

## Base URL

```
http://localhost:8000/api/v1
```

---

## Endpoints

### 1. List Notifications

Lista notificações do usuário autenticado com paginação.

**Endpoint**: `GET /notifications`

**Query Parameters**:
```
type: string (opcional) - Filtrar por tipo de notificação
read: boolean (opcional) - Filtrar por lidas/não lidas
date_from: string (opcional) - Data inicial (ISO 8601)
date_to: string (opcional) - Data final (ISO 8601)
page: number (opcional, default: 1) - Número da página
size: number (opcional, default: 20) - Itens por página
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
      "id": "notification-uuid-1",
      "user_id": "user-uuid",
      "type": "obligation_due_soon",
      "title": "Obrigação Próxima ao Vencimento",
      "message": "DAS - Documento de Arrecadação vence em 3 dias",
      "link": "/obrigacoes/550e8400-e29b-41d4-a716-446655440000",
      "metadata": {
        "obligation_id": "550e8400-e29b-41d4-a716-446655440000",
        "client_name": "Comercial Silva e Filhos LTDA",
        "due_date": "2025-11-03"
      },
      "read": false,
      "read_at": null,
      "created_at": "2025-10-30T14:30:00Z"
    },
    {
      "id": "notification-uuid-2",
      "user_id": "user-uuid",
      "type": "client_created",
      "title": "Novo Cliente",
      "message": "Cliente Tecnologia Avançada Sistemas foi cadastrado",
      "link": "/clientes/client-uuid",
      "metadata": {
        "client_id": "client-uuid",
        "client_name": "Tecnologia Avançada Sistemas LTDA"
      },
      "read": true,
      "read_at": "2025-10-30T15:00:00Z",
      "created_at": "2025-10-30T10:00:00Z"
    }
  ],
  "total": 50,
  "unread_count": 12,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

---

### 2. Get Notification

Retorna detalhes de uma notificação específica.

**Endpoint**: `GET /notifications/{notification_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "notification-uuid-1",
  "user_id": "user-uuid",
  "type": "obligation_due_soon",
  "title": "Obrigação Próxima ao Vencimento",
  "message": "DAS - Documento de Arrecadação vence em 3 dias",
  "link": "/obrigacoes/550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "obligation_id": "550e8400-e29b-41d4-a716-446655440000",
    "client_name": "Comercial Silva e Filhos LTDA",
    "due_date": "2025-11-03"
  },
  "read": false,
  "read_at": null,
  "created_at": "2025-10-30T14:30:00Z"
}
```

**Error Responses**:
- `404 Not Found`: Notificação não encontrada
- `403 Forbidden`: Notificação pertence a outro usuário

---

### 3. Create Notification

Cria uma notificação para um usuário (admin/func only).

**Endpoint**: `POST /notifications`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "user_id": "user-uuid",
  "type": "system_alert",
  "title": "Manutenção Programada",
  "message": "Sistema ficará indisponível das 02:00 às 04:00",
  "link": null,
  "metadata": {
    "scheduled_time": "2025-11-01T02:00:00Z"
  }
}
```

**Response** (201 Created):
```json
{
  "id": "notification-uuid",
  "user_id": "user-uuid",
  "type": "system_alert",
  "title": "Manutenção Programada",
  "message": "Sistema ficará indisponível das 02:00 às 04:00",
  "link": null,
  "metadata": {
    "scheduled_time": "2025-11-01T02:00:00Z"
  },
  "read": false,
  "read_at": null,
  "created_at": "2025-10-30T14:30:00Z"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Usuário não encontrado
- `422 Unprocessable Entity`: Dados inválidos

---

### 4. Create Bulk Notifications

Cria notificações para múltiplos usuários (admin only).

**Endpoint**: `POST /notifications/bulk`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "user_ids": ["user-uuid-1", "user-uuid-2", "user-uuid-3"],
  "type": "system_alert",
  "title": "Atualização do Sistema",
  "message": "Nova versão disponível com melhorias de performance",
  "link": "/changelog",
  "metadata": {
    "version": "2.0.0"
  }
}
```

**Response** (201 Created):
```json
{
  "created_count": 3,
  "notifications": [
    {
      "id": "notification-uuid-1",
      "user_id": "user-uuid-1",
      ...
    },
    {
      "id": "notification-uuid-2",
      "user_id": "user-uuid-2",
      ...
    },
    {
      "id": "notification-uuid-3",
      "user_id": "user-uuid-3",
      ...
    }
  ]
}
```

**Error Responses**:
- `403 Forbidden`: Apenas admin
- `422 Unprocessable Entity`: Dados inválidos

---

### 5. Mark as Read

Marca uma notificação como lida.

**Endpoint**: `PATCH /notifications/{notification_id}/read`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body** (opcional):
```json
{}
```

**Response** (200 OK):
```json
{
  "id": "notification-uuid-1",
  "user_id": "user-uuid",
  "type": "obligation_due_soon",
  "title": "Obrigação Próxima ao Vencimento",
  "message": "DAS - Documento de Arrecadação vence em 3 dias",
  "link": "/obrigacoes/550e8400-e29b-41d4-a716-446655440000",
  "metadata": {...},
  "read": true,
  "read_at": "2025-10-30T15:30:00Z",
  "created_at": "2025-10-30T14:30:00Z"
}
```

**Error Responses**:
- `404 Not Found`: Notificação não encontrada
- `403 Forbidden`: Notificação pertence a outro usuário

---

### 6. Mark as Unread

Marca uma notificação como não lida.

**Endpoint**: `PATCH /notifications/{notification_id}/unread`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "notification-uuid-1",
  "read": false,
  "read_at": null,
  ...
}
```

---

### 7. Mark All as Read

Marca todas as notificações do usuário como lidas.

**Endpoint**: `POST /notifications/mark-all-read`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body** (opcional):
```json
{}
```

**Response** (200 OK):
```json
{
  "marked_count": 12,
  "message": "All notifications marked as read"
}
```

---

### 8. Delete Notification

Remove uma notificação (soft delete).

**Endpoint**: `DELETE /notifications/{notification_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Notification deleted successfully"
}
```

**Error Responses**:
- `404 Not Found`: Notificação não encontrada
- `403 Forbidden`: Notificação pertence a outro usuário

---

### 9. Get Statistics

Retorna estatísticas de notificações do usuário.

**Endpoint**: `GET /notifications/statistics`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "total": 50,
  "unread": 12,
  "by_type": {
    "obligation_created": 5,
    "obligation_due_soon": 8,
    "obligation_overdue": 2,
    "obligation_completed": 15,
    "client_created": 10,
    "client_updated": 5,
    "system_alert": 5
  },
  "today_count": 8,
  "this_week_count": 25
}
```

---

### 10. Get Unread Count

Retorna apenas a contagem de notificações não lidas (endpoint rápido).

**Endpoint**: `GET /notifications/unread-count`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "count": 12
}
```

---

## Notification Types

### Obligation Related

```typescript
OBLIGATION_CREATED = "obligation_created"        // Nova obrigação criada
OBLIGATION_DUE_SOON = "obligation_due_soon"      // Obrigação vence em breve
OBLIGATION_OVERDUE = "obligation_overdue"        // Obrigação atrasada
OBLIGATION_COMPLETED = "obligation_completed"    // Obrigação concluída
OBLIGATION_CANCELED = "obligation_canceled"      // Obrigação cancelada
```

### Client Related

```typescript
CLIENT_CREATED = "client_created"                // Novo cliente cadastrado
CLIENT_UPDATED = "client_updated"                // Cliente atualizado
CLIENT_DOCUMENT_UPLOADED = "client_document_uploaded" // Documento enviado
```

### User Related

```typescript
USER_MENTION = "user_mention"                    // Usuário mencionado
USER_ASSIGNED = "user_assigned"                  // Usuário atribuído
```

### System

```typescript
SYSTEM_ALERT = "system_alert"                    // Alerta do sistema
SYSTEM_MAINTENANCE = "system_maintenance"        // Manutenção programada
```

---

## Metadata Examples

### Obligation Notification

```json
{
  "obligation_id": "uuid",
  "client_id": "uuid",
  "client_name": "Empresa LTDA",
  "obligation_type": "DAS_MENSAL",
  "due_date": "2025-11-20",
  "days_until_due": 3
}
```

### Client Notification

```json
{
  "client_id": "uuid",
  "client_name": "Empresa LTDA",
  "client_cnpj": "12.345.678/0001-90",
  "action": "created" | "updated"
}
```

### System Notification

```json
{
  "severity": "info" | "warning" | "error",
  "scheduled_time": "2025-11-01T02:00:00Z",
  "version": "2.0.0"
}
```

---

## Business Rules

### Auto-generation

Notificações são geradas automaticamente para:
- Obrigações criadas
- Obrigações próximas ao vencimento (7, 3, 1 dia antes)
- Obrigações atrasadas (diariamente)
- Obrigações concluídas
- Novos clientes cadastrados

### Retention

- Notificações lidas são mantidas por 90 dias
- Notificações não lidas são mantidas indefinidamente
- Admin pode configurar retenção personalizada

### Priority

Notificações são ordenadas por:
1. Não lidas primeiro
2. Data de criação (mais recentes primeiro)

---

## WebSocket Integration

Quando uma notificação é criada, ela é enviada automaticamente via WebSocket:

```json
{
  "type": "notification",
  "data": {
    "id": "notification-uuid",
    "type": "obligation_due_soon",
    "title": "Obrigação Próxima ao Vencimento",
    "message": "DAS vence em 3 dias",
    ...
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

Ver [websocket-api.md](./websocket-api.md) para detalhes completos.

---

## Permissions

| Endpoint | Admin | Func | Cliente |
|----------|-------|------|---------|
| GET /notifications | ✅ | ✅ | ✅ |
| GET /notifications/:id | ✅ | ✅ | ✅ (próprias) |
| POST /notifications | ✅ | ✅ | ❌ |
| POST /notifications/bulk | ✅ | ❌ | ❌ |
| PATCH /notifications/:id/read | ✅ | ✅ | ✅ (próprias) |
| PATCH /notifications/:id/unread | ✅ | ✅ | ✅ (próprias) |
| POST /notifications/mark-all-read | ✅ | ✅ | ✅ |
| DELETE /notifications/:id | ✅ | ✅ | ✅ (próprias) |
| GET /notifications/statistics | ✅ | ✅ | ✅ |
| GET /notifications/unread-count | ✅ | ✅ | ✅ |

---

## Error Handling

Todos os endpoints podem retornar:

- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro interno do servidor

---

_Última atualização: 2025-10-30_
