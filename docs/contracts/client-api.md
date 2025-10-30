# Client API Contracts

Documentação completa dos contratos de API para gerenciamento de clientes.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### 1. List Clients

Lista todos os clientes com filtros e paginação.

**Endpoint**: `GET /clients`

**Query Parameters**:
```
query: string (opcional) - Busca por razão social ou CNPJ
status: string (opcional) - Filtrar por status (ativo, inativo, pendente)
regime_tributario: string (opcional) - Filtrar por regime tributário
tipo_empresa: string (opcional) - Filtrar por tipo de empresa
starts_with: string (opcional) - Filtrar por letra inicial da razão social (A-Z)
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
      "razao_social": "Empresa Exemplo LTDA",
      "nome_fantasia": "Empresa Exemplo",
      "cnpj": "12.345.678/0001-90",
      "email": "contato@empresa.com",
      "status": "ativo",
      "honorarios_mensais": 1500.00,
      "regime_tributario": "simples_nacional",
      "tipo_empresa": "comercio",
      "created_at": "2025-10-30T10:00:00Z",
      "updated_at": "2025-10-30T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

---

### 2. Get Client

Retorna detalhes completos de um cliente.

**Endpoint**: `GET /clients/{client_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "razao_social": "Empresa Exemplo LTDA",
  "nome_fantasia": "Empresa Exemplo",
  "cnpj": "12.345.678/0001-90",
  "inscricao_estadual": "123.456.789.123",
  "inscricao_municipal": "123456",
  "email": "contato@empresa.com",
  "telefone": "(11) 3333-4444",
  "celular": "(11) 98888-7777",
  "cep": "01310-100",
  "logradouro": "Avenida Paulista",
  "numero": "1000",
  "complemento": "Sala 101",
  "bairro": "Bela Vista",
  "cidade": "São Paulo",
  "uf": "SP",
  "honorarios_mensais": 1500.00,
  "dia_vencimento": 10,
  "regime_tributario": "simples_nacional",
  "tipo_empresa": "comercio",
  "data_abertura": "2020-01-15",
  "responsavel_nome": "João Silva",
  "responsavel_cpf": "123.456.789-00",
  "responsavel_email": "joao@empresa.com",
  "responsavel_telefone": "(11) 99999-8888",
  "observacoes": "Cliente preferencial",
  "status": "ativo",
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T10:00:00Z"
}
```

**Error Responses**:
- `404 Not Found`: Cliente não encontrado

---

### 3. Create Client

Cria um novo cliente (admin ou func only).

**Endpoint**: `POST /clients`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "razao_social": "Empresa Exemplo LTDA",
  "nome_fantasia": "Empresa Exemplo",
  "cnpj": "12.345.678/0001-90",
  "inscricao_estadual": "123.456.789.123",
  "inscricao_municipal": "123456",
  "email": "contato@empresa.com",
  "telefone": "(11) 3333-4444",
  "celular": "(11) 98888-7777",
  "cep": "01310-100",
  "logradouro": "Avenida Paulista",
  "numero": "1000",
  "complemento": "Sala 101",
  "bairro": "Bela Vista",
  "cidade": "São Paulo",
  "uf": "SP",
  "honorarios_mensais": 1500.00,
  "dia_vencimento": 10,
  "regime_tributario": "simples_nacional",
  "tipo_empresa": "comercio",
  "data_abertura": "2020-01-15",
  "responsavel_nome": "João Silva",
  "responsavel_cpf": "123.456.789-00",
  "responsavel_email": "joao@empresa.com",
  "responsavel_telefone": "(11) 99999-8888",
  "observacoes": "Cliente preferencial"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "razao_social": "Empresa Exemplo LTDA",
  ...
  "status": "pendente",
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T10:00:00Z"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `409 Conflict`: CNPJ já cadastrado
- `422 Unprocessable Entity`: Dados de entrada inválidos

---

### 4. Update Client

Atualiza um cliente existente (admin ou func only).

**Endpoint**: `PUT /clients/{client_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
  "razao_social": "Empresa Exemplo LTDA Atualizada",
  "honorarios_mensais": 2000.00,
  "status": "ativo"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "razao_social": "Empresa Exemplo LTDA Atualizada",
  ...
  "honorarios_mensais": 2000.00,
  "status": "ativo",
  "updated_at": "2025-10-30T11:00:00Z"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Cliente não encontrado
- `409 Conflict`: CNPJ já existe (se alterado)

---

### 5. Delete Client

Remove um cliente (soft delete, admin only).

**Endpoint**: `DELETE /clients/{client_id}`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Client deleted successfully"
}
```

**Error Responses**:
- `403 Forbidden`: Usuário não tem permissão (apenas admin)
- `404 Not Found`: Cliente não encontrado

---

### 6. Search Clients

Busca rápida de clientes para autocomplete.

**Endpoint**: `GET /clients/search`

**Query Parameters**:
```
q: string (obrigatório) - Termo de busca
limit: number (opcional, default: 10) - Máximo de resultados
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
      "razao_social": "Empresa Exemplo LTDA",
      "cnpj": "12.345.678/0001-90"
    }
  ]
}
```

---

## Data Types

### ClientStatus Enum

```typescript
enum ClientStatus {
  ATIVO = "ativo",       // Cliente ativo
  INATIVO = "inativo",   // Cliente inativo
  PENDENTE = "pendente"  // Aguardando ativação
}
```

### RegimeTributario Enum

```typescript
enum RegimeTributario {
  SIMPLES_NACIONAL = "simples_nacional",
  LUCRO_PRESUMIDO = "lucro_presumido",
  LUCRO_REAL = "lucro_real",
  MEI = "mei"
}
```

### TipoEmpresa Enum

```typescript
enum TipoEmpresa {
  COMERCIO = "comercio",     // Comércio
  SERVICO = "servico",       // Prestação de serviços
  INDUSTRIA = "industria",   // Indústria
  MISTO = "misto"            // Atividades mistas
}
```

---

## Business Rules

### CNPJ Validation

- Deve conter exatamente 14 dígitos
- Deve ser único no sistema
- Formato armazenado: `XX.XXX.XXX/XXXX-XX`

### Honorários

- Valor mínimo: R$ 0,00
- Sem valor máximo
- Duas casas decimais

### Dia de Vencimento

- Deve estar entre 1 e 31
- Se dia não existir no mês (ex: 31 de fevereiro), usar último dia do mês

### Status

- Novo cliente inicia como `PENDENTE`
- Apenas admin pode alterar status
- Cliente `INATIVO` não pode ter obrigações geradas

---

## Error Handling

Todos os endpoints podem retornar:

- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro interno do servidor

---

## Permissions

| Endpoint | Admin | Func | Cliente |
|----------|-------|------|---------|
| GET /clients | ✅ | ✅ | ❌ |
| GET /clients/{id} | ✅ | ✅ | ✅ (próprio) |
| POST /clients | ✅ | ✅ | ❌ |
| PUT /clients/{id} | ✅ | ✅ | ❌ |
| DELETE /clients/{id} | ✅ | ❌ | ❌ |
| GET /clients/search | ✅ | ✅ | ❌ |

---

_Última atualização: 2025-10-30_
