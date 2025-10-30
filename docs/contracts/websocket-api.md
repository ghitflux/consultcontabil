# WebSocket API Contracts

Documentação completa da API WebSocket para comunicação em tempo real.

## Connection URL

```
ws://localhost:8000/api/v1/ws/{access_token}
```

**Production**:
```
wss://api.contabilconsult.com/api/v1/ws/{access_token}
```

---

## Connection Flow

### 1. Client Connects

Cliente conecta passando o access token na URL:

```javascript
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${accessToken}`);
```

### 2. Server Validates

Backend valida o token:
- Decodifica JWT
- Verifica expiração
- Extrai `user_id` e `role`
- Se inválido: fecha conexão com código `1008` (Policy Violation)

### 3. Connection Accepted

Backend aceita conexão e envia mensagem de boas-vindas:

```json
{
  "type": "connected",
  "message": "WebSocket connected successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "admin",
  "timestamp": "2025-10-30T14:30:00Z"
}
```

### 4. Keep-Alive

Cliente envia ping periodicamente (recomendado: a cada 30s):

```
Client → Server: "ping"
Server → Client: "pong"
```

### 5. Receive Events

Cliente recebe eventos em tempo real conforme acontecem no sistema.

---

## Event Types

### 1. Notification Event

Enviado quando uma nova notificação é criada para o usuário.

**Type**: `notification`

**Example**:
```json
{
  "type": "notification",
  "data": {
    "id": "notification-uuid",
    "user_id": "user-uuid",
    "type": "obligation_due_soon",
    "title": "Obrigação Próxima ao Vencimento",
    "message": "DAS - Documento de Arrecadação vence em 3 dias",
    "link": "/obrigacoes/obligation-uuid",
    "metadata": {
      "obligation_id": "obligation-uuid",
      "client_name": "Comercial Silva e Filhos LTDA",
      "due_date": "2025-11-03",
      "days_until_due": 3
    },
    "read": false,
    "read_at": null,
    "created_at": "2025-10-30T14:30:00Z"
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

**When Sent**:
- Nova obrigação criada para um cliente do usuário
- Obrigação próxima ao vencimento
- Obrigação atrasada
- Obrigação concluída
- Cliente criado/atualizado
- Sistema: alertas e manutenções

---

### 2. Obligation Update Event

Enviado quando uma obrigação é atualizada.

**Type**: `obligation_update`

**Example**:
```json
{
  "type": "obligation_update",
  "data": {
    "id": "obligation-uuid",
    "client_id": "client-uuid",
    "client_name": "Comercial Silva e Filhos LTDA",
    "obligation_type_name": "DAS - Documento de Arrecadação",
    "obligation_type_code": "DAS_MENSAL",
    "status": "concluida",
    "priority": "media",
    "due_date": "2025-11-20",
    "completed_at": "2025-10-30T14:30:00Z",
    "completed_by_name": "João Silva",
    "action": "completed"
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

**Actions**:
- `created`: Nova obrigação criada
- `updated`: Obrigação atualizada (status, prioridade, etc)
- `completed`: Obrigação marcada como concluída
- `canceled`: Obrigação cancelada

**When Sent**:
- Obrigação criada
- Status alterado
- Upload de comprovante
- Obrigação cancelada

---

### 3. System Event

Enviado para alertas e mensagens do sistema.

**Type**: `system`

**Example**:
```json
{
  "type": "system",
  "data": {
    "message": "Sistema será atualizado em 5 minutos",
    "severity": "warning",
    "action_required": false,
    "scheduled_time": "2025-11-01T02:00:00Z"
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

**Severities**:
- `info`: Informação geral
- `warning`: Aviso importante
- `error`: Erro ou problema crítico

**When Sent**:
- Manutenção programada
- Atualizações do sistema
- Problemas técnicos
- Mudanças de configuração

---

### 4. Client Update Event

Enviado quando um cliente é criado ou atualizado.

**Type**: `client_update`

**Example**:
```json
{
  "type": "client_update",
  "data": {
    "id": "client-uuid",
    "razao_social": "Comercial Silva e Filhos LTDA",
    "cnpj": "12.345.678/0001-90",
    "status": "ativo",
    "action": "created"
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

**Actions**:
- `created`: Novo cliente cadastrado
- `updated`: Cliente atualizado
- `deleted`: Cliente removido

---

### 5. User Mention Event

Enviado quando um usuário é mencionado em comentário/nota.

**Type**: `user_mention`

**Example**:
```json
{
  "type": "user_mention",
  "data": {
    "mentioned_by": "João Silva",
    "mentioned_by_id": "user-uuid",
    "context": "obligation",
    "context_id": "obligation-uuid",
    "message": "@maria precisa revisar este DAS",
    "link": "/obrigacoes/obligation-uuid"
  },
  "timestamp": "2025-10-30T14:30:00Z"
}
```

---

## Broadcasting Modes

### 1. Personal Message

Mensagem enviada para um usuário específico:

```python
await manager.send_personal_message(user_id, message)
```

**Use Cases**:
- Notificações pessoais
- Obrigações específicas do cliente do usuário
- Menções diretas

### 2. Broadcast to Role

Mensagem enviada para todos usuários de um role:

```python
await manager.broadcast_to_role("admin", message)
```

**Use Cases**:
- Alertas do sistema (admin/func)
- Novas obrigações geradas (admin/func)
- Manutenção programada (todos)

### 3. Broadcast All

Mensagem enviada para todos usuários conectados:

```python
await manager.broadcast(message)
```

**Use Cases**:
- Alertas críticos
- Mensagens do sistema
- Atualizações importantes

---

## Client Implementation

### JavaScript/TypeScript

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  private token: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  constructor(token: string) {
    this.token = token;
  }

  connect() {
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/${this.token}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.emit('connected', {});
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.emit(message.type, message.data);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.emit('disconnected', {});
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };

    // Start ping interval
    setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
      }
    }, 30000); // 30 seconds
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Max reconnect attempts reached');
      this.emit('max_reconnect_reached', {});
    }
  }

  on(eventType: string, callback: (data: any) => void) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }
    this.listeners.get(eventType)!.add(callback);
  }

  off(eventType: string, callback: (data: any) => void) {
    this.listeners.get(eventType)?.delete(callback);
  }

  private emit(eventType: string, data: any) {
    this.listeners.get(eventType)?.forEach(callback => callback(data));
  }

  disconnect() {
    this.ws?.close();
  }
}

// Usage
const wsClient = new WebSocketClient(accessToken);

wsClient.on('connected', (data) => {
  console.log('Connected:', data);
});

wsClient.on('notification', (notification) => {
  console.log('New notification:', notification);
  // Show toast or update UI
  toast.info(notification.title, {
    description: notification.message,
  });
});

wsClient.on('obligation_update', (data) => {
  console.log('Obligation updated:', data);
  // Update obligation list in UI
  queryClient.invalidateQueries(['obligations']);
});

wsClient.on('system', (data) => {
  console.log('System message:', data);
  if (data.severity === 'error') {
    toast.error('Erro do Sistema', {
      description: data.message,
    });
  }
});

wsClient.connect();

// Cleanup
useEffect(() => {
  return () => {
    wsClient.disconnect();
  };
}, []);
```

---

## Connection States

### Open

```
ws.readyState === WebSocket.OPEN (1)
```

Connection is active. Can send and receive messages.

### Connecting

```
ws.readyState === WebSocket.CONNECTING (0)
```

Connection is being established.

### Closing

```
ws.readyState === WebSocket.CLOSING (2)
```

Connection is being closed.

### Closed

```
ws.readyState === WebSocket.CLOSED (3)
```

Connection is closed. Should attempt reconnection.

---

## Close Codes

| Code | Name | Description |
|------|------|-------------|
| 1000 | Normal Closure | Normal disconnection |
| 1001 | Going Away | Browser navigating away |
| 1008 | Policy Violation | Token invalid/expired |
| 1011 | Internal Error | Server error |

---

## Best Practices

### 1. Auto-Reconnect

Implement exponential backoff for reconnections:

```typescript
const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
```

### 2. Ping/Pong

Send ping every 30 seconds to keep connection alive:

```typescript
setInterval(() => {
  if (ws?.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);
```

### 3. Token Refresh

Before token expires, disconnect and reconnect with new token:

```typescript
// When token is about to expire
wsClient.disconnect();
const newToken = await refreshToken();
wsClient = new WebSocketClient(newToken);
wsClient.connect();
```

### 4. Message Queue

Queue messages if connection is lost:

```typescript
private messageQueue: any[] = [];

send(message: any) {
  if (this.ws?.readyState === WebSocket.OPEN) {
    this.ws.send(JSON.stringify(message));
  } else {
    this.messageQueue.push(message);
  }
}

// On reconnect, flush queue
this.ws.onopen = () => {
  while (this.messageQueue.length > 0) {
    this.send(this.messageQueue.shift());
  }
};
```

### 5. Memory Management

Remove event listeners when component unmounts:

```typescript
useEffect(() => {
  const handler = (data) => {
    // Handle notification
  };

  wsClient.on('notification', handler);

  return () => {
    wsClient.off('notification', handler);
  };
}, []);
```

---

## Security

### 1. Token Validation

- Token is validated on connection
- Invalid tokens are rejected with code `1008`
- Expired tokens close connection

### 2. User Isolation

- Users only receive their own notifications
- Role-based broadcasting for system messages
- No cross-user data leakage

### 3. Rate Limiting

- Max 100 messages per minute per connection
- Ping/pong not counted
- Exceeded limit: temporary disconnect

---

## Monitoring

### Server Side

```python
# Connection metrics
active_connections = len(manager.active_connections)
connections_by_role = {
    "admin": len([r for r in manager.user_roles.values() if r == "admin"]),
    "func": len([r for r in manager.user_roles.values() if r == "func"]),
    "cliente": len([r for r in manager.user_roles.values() if r == "cliente"]),
}

# Message metrics
messages_sent_total = ...
messages_sent_per_minute = ...
```

### Client Side

```typescript
// Track connection state
const [connectionState, setConnectionState] = useState<
  'connecting' | 'connected' | 'disconnected' | 'error'
>('disconnected');

// Track reconnection attempts
const [reconnectAttempts, setReconnectAttempts] = useState(0);

// Track messages received
const [messagesReceived, setMessagesReceived] = useState(0);
```

---

## Troubleshooting

### Connection Rejected

**Symptom**: Connection closes immediately with code `1008`

**Cause**: Invalid or expired token

**Solution**:
- Check token validity
- Refresh token before connecting
- Verify token format

### Frequent Disconnections

**Symptom**: Connection drops every few minutes

**Cause**:
- Network issues
- Missing ping/pong
- Server restart

**Solution**:
- Implement ping/pong
- Add auto-reconnect
- Check network stability

### Messages Not Received

**Symptom**: Not receiving expected events

**Cause**:
- Event listener not registered
- Connection closed
- User not authorized

**Solution**:
- Check event listener registration
- Verify connection state
- Check user permissions

---

## Testing

### Manual Testing

```bash
# Connect with wscat
npm install -g wscat

# Connect
wscat -c "ws://localhost:8000/api/v1/ws/YOUR_ACCESS_TOKEN"

# Send ping
> ping

# Receive pong
< pong

# Receive notification
< {"type":"notification","data":{...},"timestamp":"..."}
```

### Automated Testing

```python
# Backend test
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

def test_websocket_connection(client: TestClient, admin_token: str):
    with client.websocket_connect(f"/api/v1/ws/{admin_token}") as ws:
        # Receive welcome message
        data = ws.receive_json()
        assert data["type"] == "connected"

        # Send ping
        ws.send_text("ping")

        # Receive pong
        response = ws.receive_text()
        assert response == "pong"
```

---

_Última atualização: 2025-10-30_
