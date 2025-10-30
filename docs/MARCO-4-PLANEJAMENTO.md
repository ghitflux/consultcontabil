# Marco 4 - OBRIGAÇÕES + NOTIFICAÇÕES - PLANEJAMENTO COMPLETO

## 🎯 Visão Geral

O Marco 4 implementa o sistema completo de obrigações fiscais com notificações em tempo real via WebSocket. É o coração do sistema, onde a inteligência de negócio se concentra.

### Objetivos Principais

1. **CRUD de Obrigações Fiscais**: Gerenciamento completo de obrigações
2. **Geração Automática**: Factory pattern + Strategy pattern para regras por tipo de empresa
3. **Processo de Baixa**: Upload obrigatório de comprovante
4. **Timeline de Eventos**: Histórico completo de cada obrigação
5. **Notificações Real-Time**: WebSocket para alertas instantâneos
6. **Portal do Cliente**: Visão limitada para clientes
7. **Notification Center**: UI completa com badge, dropdown e gerenciamento

---

## 📊 Métricas de Entrega

- **Blocos**: 12 blocos atômicos
- **Tempo Estimado**: 40-45 horas
- **Endpoints Backend**: ~15 novos
- **Páginas Frontend**: 3 (obrigações, portal, notification center)
- **WebSocket Events**: 6 tipos
- **Cobertura de Testes**: Mínimo 70%
- **Design Patterns**: Strategy, Factory, Observer

---

## 🏗️ Arquitetura

### Backend (FastAPI)

```
apps/api/app/
├── schemas/
│   ├── obligation.py           # Schemas Pydantic
│   └── notification.py         # Schemas de notificação
├── db/
│   ├── models/
│   │   ├── obligation.py       # Model principal
│   │   ├── obligation_type.py  # Tipos de obrigações
│   │   ├── obligation_event.py # Timeline
│   │   └── notification.py     # Notificações
│   └── repositories/
│       ├── obligation.py
│       └── notification.py
├── services/
│   ├── obligation/
│   │   ├── generator.py        # Geração mensal
│   │   ├── processor.py        # Baixa de obrigações
│   │   └── notifier.py         # Envio de notificações
│   └── notification.py
├── patterns/
│   ├── strategies/
│   │   ├── base.py
│   │   ├── commerce_rule.py    # Comércio
│   │   ├── service_rule.py     # Serviços
│   │   ├── industry_rule.py    # Indústria
│   │   └── mei_rule.py         # MEI
│   └── factories/
│       └── obligation_factory.py
├── websockets/
│   ├── manager.py              # ConnectionManager
│   ├── handlers.py             # Event handlers
│   └── events.py               # Event types
└── api/v1/routes/
    ├── obligations.py
    ├── notifications.py
    └── websocket.py
```

### Frontend (Next.js)

```
apps/web/
├── src/
│   ├── types/
│   │   ├── obligation.ts
│   │   └── notification.ts
│   ├── lib/
│   │   ├── api/endpoints/
│   │   │   ├── obligations.ts
│   │   │   └── notifications.ts
│   │   └── ws/
│   │       ├── client.ts       # WebSocket client
│   │       └── events.ts       # Event handlers
│   ├── hooks/
│   │   ├── useObligations.ts
│   │   ├── useNotifications.ts
│   │   └── useWebSocket.ts
│   └── components/
│       ├── ui/
│       │   └── NotificationBell.tsx
│       └── features/
│           ├── obrigacoes/
│           │   ├── ObligationsTable.tsx
│           │   ├── ObligationCard.tsx
│           │   ├── ObligationFilters.tsx
│           │   ├── ObligationTimeline.tsx
│           │   └── ReceiptUploadModal.tsx
│           └── notifications/
│               ├── NotificationCenter.tsx
│               ├── NotificationList.tsx
│               └── NotificationItem.tsx
└── app/
    ├── (dashboard)/
    │   ├── obrigacoes/page.tsx
    │   └── layout.tsx          # Atualizar header com bell
    └── (portal)/
        └── obrigacoes/page.tsx
```

---

## 📦 Blocos de Desenvolvimento

### Bloco 4.1: Contracts de Obrigações e Notificações

**Duração**: 2-3 horas
**Dependências**: Marco 3 completo

**Objetivos**:
- Definir schemas Pydantic para obrigações
- Definir schemas de notificações
- Criar types TypeScript correspondentes
- Documentar contratos da API

**Entregáveis**:
```
apps/api/app/schemas/
✓ obligation.py
✓ notification.py

apps/web/src/types/
✓ obligation.ts
✓ notification.ts

docs/contracts/
✓ obligation-api.md
✓ notification-api.md
✓ websocket-api.md
```

**Schemas Principais**:

```python
# obligation.py
class ObligationStatus(str, Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"

class ObligationPriority(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

class ObligationCreate(BaseModel):
    client_id: UUID
    obligation_type_id: UUID
    due_date: date
    description: Optional[str] = None
    priority: ObligationPriority = ObligationPriority.MEDIA

class ObligationResponse(BaseModel):
    id: UUID
    client_id: UUID
    client_name: str
    obligation_type: ObligationTypeResponse
    due_date: date
    status: ObligationStatus
    priority: ObligationPriority
    description: Optional[str] = None
    receipt_url: Optional[str] = None
    completed_at: Optional[datetime] = None
    completed_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class ObligationReceiptUpload(BaseModel):
    notes: Optional[str] = None
```

```python
# notification.py
class NotificationType(str, Enum):
    OBLIGATION_CREATED = "obligation_created"
    OBLIGATION_DUE_SOON = "obligation_due_soon"
    OBLIGATION_OVERDUE = "obligation_overdue"
    OBLIGATION_COMPLETED = "obligation_completed"
    CLIENT_CREATED = "client_created"
    SYSTEM_ALERT = "system_alert"

class NotificationCreate(BaseModel):
    user_id: UUID
    type: NotificationType
    title: str
    message: str
    link: Optional[str] = None
    metadata: Optional[dict] = None

class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    type: NotificationType
    title: str
    message: str
    link: Optional[str] = None
    metadata: Optional[dict] = None
    read: bool
    created_at: datetime
```

**Critérios de Aceite**:
- Schemas validam corretamente
- Types TypeScript sincronizados
- Documentação clara com exemplos
- Enums sincronizados backend/frontend

---

### Bloco 4.2: Models e Migrations

**Duração**: 3-4 horas
**Dependências**: Bloco 4.1

**Objetivos**:
- Models SQLAlchemy para obrigações
- Models para notificações
- Migrations Alembic
- Seed de tipos de obrigações

**Entregáveis**:
```
apps/api/app/db/models/
✓ obligation.py
✓ obligation_type.py
✓ obligation_event.py
✓ notification.py

apps/api/alembic/versions/
✓ 004_add_obligations.py
✓ 005_add_notifications.py

apps/api/scripts/
✓ seed_obligation_types.py

apps/api/tests/unit/models/
✓ test_obligation.py
✓ test_notification.py
```

**Models Principais**:

```python
# obligation.py
class Obligation(Base):
    __tablename__ = "obligations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    obligation_type_id = Column(UUID(as_uuid=True), ForeignKey("obligation_types.id"), nullable=False)

    due_date = Column(Date, nullable=False, index=True)
    status = Column(Enum(ObligationStatus), default=ObligationStatus.PENDENTE, index=True)
    priority = Column(Enum(ObligationPriority), default=ObligationPriority.MEDIA)

    description = Column(Text, nullable=True)
    receipt_url = Column(String(500), nullable=True)

    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    client = relationship("Client", back_populates="obligations")
    obligation_type = relationship("ObligationType")
    completed_by_user = relationship("User")
    events = relationship("ObligationEvent", back_populates="obligation", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_obligations_client_due', 'client_id', 'due_date'),
        Index('idx_obligations_status_due', 'status', 'due_date'),
    )

# obligation_type.py
class ObligationType(Base):
    __tablename__ = "obligation_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Aplicável para quais tipos de empresa
    applies_to_commerce = Column(Boolean, default=False)
    applies_to_service = Column(Boolean, default=False)
    applies_to_industry = Column(Boolean, default=False)
    applies_to_mei = Column(Boolean, default=False)

    # Aplicável para quais regimes
    applies_to_simples = Column(Boolean, default=False)
    applies_to_presumido = Column(Boolean, default=False)
    applies_to_real = Column(Boolean, default=False)

    # Configuração de geração
    recurrence = Column(String(20), nullable=False)  # mensal, trimestral, anual
    day_of_month = Column(Integer, nullable=True)  # 1-31
    month_of_year = Column(Integer, nullable=True)  # 1-12 (para anuais)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# obligation_event.py
class ObligationEvent(Base):
    __tablename__ = "obligation_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    obligation_id = Column(UUID(as_uuid=True), ForeignKey("obligations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    event_type = Column(String(50), nullable=False)  # created, started, completed, canceled, etc
    description = Column(Text, nullable=False)
    metadata = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    obligation = relationship("Obligation", back_populates="events")
    user = relationship("User")

# notification.py
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    type = Column(Enum(NotificationType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)
    metadata = Column(JSONB, nullable=True)

    read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User")

    __table_args__ = (
        Index('idx_notifications_user_unread', 'user_id', 'read', 'created_at'),
    )
```

**Seed de Tipos de Obrigações**:
```python
# 20+ tipos de obrigações fiscais comuns
OBLIGATION_TYPES = [
    {
        "code": "DAS_MENSAL",
        "name": "DAS - Documento de Arrecadação do Simples Nacional",
        "recurrence": "mensal",
        "day_of_month": 20,
        "applies_to_simples": True,
    },
    {
        "code": "DCTF_MENSAL",
        "name": "DCTF - Declaração de Débitos e Créditos Tributários Federais",
        "recurrence": "mensal",
        "day_of_month": 15,
        "applies_to_presumido": True,
        "applies_to_real": True,
    },
    # ... mais 18 tipos
]
```

**Critérios de Aceite**:
- Migrations executam sem erros
- Seed cria 20+ tipos de obrigações
- Relacionamentos funcionam
- Índices criados corretamente
- Soft delete implementado
- Testes unitários passam (9+ testes)

---

### Bloco 4.3: WebSocket Infrastructure (Backend)

**Duração**: 4-5 horas
**Dependências**: Bloco 4.2

**Objetivos**:
- ConnectionManager para WebSocket
- Event handlers
- Broadcast por usuário/role
- Integração com FastAPI

**Entregáveis**:
```
apps/api/app/websockets/
✓ manager.py
✓ handlers.py
✓ events.py

apps/api/app/api/v1/routes/
✓ websocket.py

apps/api/tests/integration/
✓ test_websocket.py
```

**Implementação**:

```python
# manager.py
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # user_id -> websocket
        self.user_roles: Dict[str, str] = {}  # user_id -> role

    async def connect(self, websocket: WebSocket, user_id: str, role: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_roles[user_id] = role
        logger.info(f"WebSocket connected: user={user_id}, role={role}")

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)
        self.user_roles.pop(user_id, None)
        logger.info(f"WebSocket disconnected: user={user_id}")

    async def send_personal_message(self, user_id: str, message: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

    async def broadcast(self, message: dict, exclude: Optional[List[str]] = None):
        exclude = exclude or []
        for user_id, websocket in self.active_connections.items():
            if user_id not in exclude:
                await websocket.send_json(message)

    async def broadcast_to_role(self, role: str, message: dict):
        for user_id, user_role in self.user_roles.items():
            if user_role == role:
                await self.send_personal_message(user_id, message)

manager = ConnectionManager()

# events.py
class WebSocketEvent(BaseModel):
    type: str
    data: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class NotificationEvent(WebSocketEvent):
    type: Literal["notification"] = "notification"

class ObligationUpdateEvent(WebSocketEvent):
    type: Literal["obligation_update"] = "obligation_update"

# routes/websocket.py
@router.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Validate token and get user
        payload = decode_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Connect
        await manager.connect(websocket, user_id, role)

        # Send welcome message
        await manager.send_personal_message(user_id, {
            "type": "connected",
            "message": "WebSocket connected successfully"
        })

        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Handle ping/pong or other client messages
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(user_id)
```

**Critérios de Aceite**:
- WebSocket aceita conexões autenticadas
- Mensagens pessoais funcionam
- Broadcast funciona
- Desconexão limpa estado
- Testes de integração passam

---

### Bloco 4.4: Strategy Pattern (Regras por Tipo)

**Duração**: 3-4 horas
**Dependências**: Bloco 4.2

**Objetivos**:
- Base strategy para regras de obrigações
- Implementações por tipo de empresa
- Lógica de aplicabilidade

**Entregáveis**:
```
apps/api/app/patterns/strategies/
✓ base.py
✓ commerce_rule.py
✓ service_rule.py
✓ industry_rule.py
✓ mei_rule.py

apps/api/tests/unit/patterns/
✓ test_strategies.py
```

**Implementação**:

```python
# base.py
from abc import ABC, abstractmethod
from typing import List
from datetime import date

class ObligationRule(ABC):
    """Base class for obligation generation rules"""

    @abstractmethod
    def get_applicable_types(self, client: Client) -> List[ObligationType]:
        """Returns obligation types applicable to this client"""
        pass

    @abstractmethod
    def calculate_due_date(self, obligation_type: ObligationType, reference_month: date) -> date:
        """Calculate due date for given type and month"""
        pass

    @abstractmethod
    def get_priority(self, obligation_type: ObligationType, due_date: date) -> ObligationPriority:
        """Calculate priority based on type and due date"""
        pass

# commerce_rule.py
class CommerceRule(ObligationRule):
    def get_applicable_types(self, client: Client) -> List[ObligationType]:
        obligation_types = []

        # Simples Nacional
        if client.regime_tributario == "simples_nacional":
            obligation_types.extend([
                "DAS_MENSAL",
                "DEFIS_ANUAL"
            ])

        # Lucro Presumido
        elif client.regime_tributario == "lucro_presumido":
            obligation_types.extend([
                "DCTF_MENSAL",
                "PIS_COFINS_MENSAL",
                "EFD_CONTRIBUICOES"
            ])

        # Estadual (ICMS para comércio)
        if client.uf in ["SP", "RJ", "MG"]:  # Exemplo
            obligation_types.append("SPED_FISCAL")

        return obligation_types

    def calculate_due_date(self, obligation_type: ObligationType, reference_month: date) -> date:
        # Lógica específica para comércio
        day = obligation_type.day_of_month
        month = reference_month.month + 1 if reference_month.month < 12 else 1
        year = reference_month.year if month > 1 else reference_month.year + 1

        return date(year, month, min(day, 28))  # Evitar dia 29-31

    def get_priority(self, obligation_type: ObligationType, due_date: date) -> ObligationPriority:
        days_until_due = (due_date - date.today()).days

        if days_until_due < 0:
            return ObligationPriority.URGENTE
        elif days_until_due <= 3:
            return ObligationPriority.ALTA
        elif days_until_due <= 7:
            return ObligationPriority.MEDIA
        else:
            return ObligationPriority.BAIXA

# Similar para service_rule.py, industry_rule.py, mei_rule.py
```

**Critérios de Aceite**:
- Cada strategy implementa regras específicas
- Testes cobrem casos de cada tipo
- Prioridades calculadas corretamente
- Datas de vencimento corretas

---

### Bloco 4.5: Factory de Obrigações

**Duração**: 3-4 horas
**Dependências**: Bloco 4.4

**Objetivos**:
- Factory para criar obrigações
- Integração com strategies
- Lógica de geração mensal

**Entregáveis**:
```
apps/api/app/patterns/factories/
✓ obligation_factory.py

apps/api/tests/unit/patterns/
✓ test_obligation_factory.py
```

**Implementação**:

```python
# obligation_factory.py
class ObligationFactory:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.strategies = {
            TipoEmpresa.COMERCIO: CommerceRule(),
            TipoEmpresa.SERVICO: ServiceRule(),
            TipoEmpresa.INDUSTRIA: IndustryRule(),
            TipoEmpresa.MISTO: CommerceRule(),  # Ou estratégia combinada
        }

    async def generate_for_client(
        self,
        client: Client,
        reference_month: date
    ) -> List[Obligation]:
        """Generate all obligations for a client for given month"""

        strategy = self.strategies.get(client.tipo_empresa)
        if not strategy:
            raise ValueError(f"No strategy for tipo_empresa: {client.tipo_empresa}")

        # Get applicable types
        type_codes = strategy.get_applicable_types(client)

        # Fetch ObligationType models
        obligation_types = await self.db.execute(
            select(ObligationType).where(
                ObligationType.code.in_(type_codes),
                ObligationType.is_active == True
            )
        )
        obligation_types = obligation_types.scalars().all()

        # Create obligations
        obligations = []
        for ob_type in obligation_types:
            due_date = strategy.calculate_due_date(ob_type, reference_month)
            priority = strategy.get_priority(ob_type, due_date)

            obligation = Obligation(
                client_id=client.id,
                obligation_type_id=ob_type.id,
                due_date=due_date,
                priority=priority,
                status=ObligationStatus.PENDENTE,
                description=f"Referência: {reference_month.strftime('%m/%Y')}"
            )
            obligations.append(obligation)

        return obligations

    async def generate_bulk(
        self,
        reference_month: date,
        client_ids: Optional[List[UUID]] = None
    ) -> int:
        """Generate obligations for multiple clients"""

        # Get clients
        query = select(Client).where(
            Client.status == "ativo",
            Client.deleted_at.is_(None)
        )
        if client_ids:
            query = query.where(Client.id.in_(client_ids))

        result = await self.db.execute(query)
        clients = result.scalars().all()

        total_created = 0
        for client in clients:
            obligations = await self.generate_for_client(client, reference_month)

            for ob in obligations:
                self.db.add(ob)

            total_created += len(obligations)

        await self.db.commit()
        return total_created
```

**Critérios de Aceite**:
- Factory cria obrigações corretas por tipo
- Geração em massa funciona
- Strategies são aplicadas corretamente
- Testes cobrem cenários complexos

---

### Bloco 4.6: Geração Mensal Automática

**Duração**: 3 horas
**Dependências**: Bloco 4.5

**Objetivos**:
- Endpoint para geração manual
- Job agendado (cron-like)
- Validações e logs

**Entregáveis**:
```
apps/api/app/services/obligation/
✓ generator.py

apps/api/app/api/v1/routes/
✓ obligations.py (POST /generate)

apps/api/app/jobs/
✓ monthly_obligations.py

apps/api/tests/integration/
✓ test_obligation_generation.py
```

**Implementação**:

```python
# services/obligation/generator.py
class ObligationGeneratorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.factory = ObligationFactory(db)

    async def generate_monthly(
        self,
        reference_month: Optional[date] = None
    ) -> Dict[str, Any]:
        """Generate obligations for all active clients"""

        if not reference_month:
            # Next month by default
            today = date.today()
            if today.month == 12:
                reference_month = date(today.year + 1, 1, 1)
            else:
                reference_month = date(today.year, today.month + 1, 1)

        # Check if already generated
        existing = await self.db.execute(
            select(func.count(Obligation.id)).where(
                extract('month', Obligation.due_date) == reference_month.month,
                extract('year', Obligation.due_date) == reference_month.year
            )
        )
        existing_count = existing.scalar()

        if existing_count > 0:
            raise ValueError(f"Obligations already generated for {reference_month.strftime('%m/%Y')}")

        # Generate
        logger.info(f"Starting obligation generation for {reference_month}")
        total_created = await self.factory.generate_bulk(reference_month)

        logger.info(f"Generated {total_created} obligations")

        return {
            "reference_month": reference_month,
            "total_created": total_created,
            "status": "success"
        }

# routes/obligations.py
@router.post("/generate", dependencies=[Depends(require_role(["admin"]))])
async def generate_obligations(
    reference_month: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate obligations for a given month (admin only)"""

    service = ObligationGeneratorService(db)
    result = await service.generate_monthly(reference_month)

    # Audit log
    await audit_service.log_action(
        user=current_user,
        action="generate_obligations",
        entity="obligation",
        payload=result
    )

    return result
```

**Critérios de Aceite**:
- Endpoint gera obrigações corretamente
- Validação de duplicatas funciona
- Auditoria registrada
- Testes cobrem casos de sucesso e erro

---

### Bloco 4.7: Processo de Baixa

**Duração**: 4 horas
**Dependências**: Bloco 4.3, 4.6

**Objetivos**:
- Upload obrigatório de comprovante
- Mudança de status para concluída
- Notificação WebSocket
- Event na timeline

**Entregáveis**:
```
apps/api/app/services/obligation/
✓ processor.py

apps/api/app/api/v1/routes/
✓ obligations.py (POST /:id/receipt)

apps/api/tests/integration/
✓ test_obligation_receipt.py
```

**Implementação**:

```python
# services/obligation/processor.py
class ObligationProcessorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_storage = FileStorageService()
        self.notifier = NotificationService(db)

    async def complete_obligation(
        self,
        obligation_id: UUID,
        user: User,
        receipt_file: UploadFile,
        notes: Optional[str] = None
    ) -> Obligation:
        """Complete an obligation with receipt upload"""

        # Get obligation
        obligation = await self.db.get(Obligation, obligation_id)
        if not obligation:
            raise HTTPException(404, "Obligation not found")

        if obligation.status == ObligationStatus.CONCLUIDA:
            raise HTTPException(400, "Obligation already completed")

        # Upload receipt
        receipt_url = await self.file_storage.save_file(
            file=receipt_file,
            entity_type="obligation",
            entity_id=str(obligation_id),
            allowed_extensions=[".pdf", ".jpg", ".jpeg", ".png"]
        )

        # Update obligation
        obligation.status = ObligationStatus.CONCLUIDA
        obligation.receipt_url = receipt_url
        obligation.completed_at = datetime.utcnow()
        obligation.completed_by = user.id

        # Create event
        event = ObligationEvent(
            obligation_id=obligation_id,
            user_id=user.id,
            event_type="completed",
            description=f"Obrigação concluída por {user.name}",
            metadata={"notes": notes} if notes else None
        )
        self.db.add(event)

        await self.db.commit()
        await self.db.refresh(obligation)

        # Send notification via WebSocket
        await self._notify_completion(obligation, user)

        return obligation

    async def _notify_completion(self, obligation: Obligation, user: User):
        """Send WebSocket notification"""

        # Create notification record
        notification = await self.notifier.create_notification(
            user_id=obligation.client.user_id,  # Notify client owner
            type=NotificationType.OBLIGATION_COMPLETED,
            title="Obrigação Concluída",
            message=f"{obligation.obligation_type.name} foi concluída",
            link=f"/obrigacoes/{obligation.id}",
            metadata={"obligation_id": str(obligation.id)}
        )

        # Send via WebSocket
        from app.websockets.manager import manager
        await manager.send_personal_message(
            str(obligation.client.user_id),
            {
                "type": "notification",
                "data": NotificationResponse.from_orm(notification).dict()
            }
        )

# routes/obligations.py
@router.post("/{obligation_id}/receipt")
async def upload_receipt(
    obligation_id: UUID,
    file: UploadFile = File(...),
    notes: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload receipt and complete obligation"""

    service = ObligationProcessorService(db)
    obligation = await service.complete_obligation(
        obligation_id=obligation_id,
        user=current_user,
        receipt_file=file,
        notes=notes
    )

    return ObligationResponse.from_orm(obligation)
```

**Critérios de Aceite**:
- Upload funciona e valida extensões
- Status muda para concluída
- Event criado na timeline
- Notificação enviada via WebSocket
- Testes passam

---

### Bloco 4.8: Timeline de Eventos

**Duração**: 2-3 horas
**Dependências**: Bloco 4.7

**Objetivos**:
- Endpoint de eventos
- Formatação de timeline
- Integração com frontend

**Entregáveis**:
```
apps/api/app/api/v1/routes/
✓ obligations.py (GET /:id/events)

apps/api/tests/integration/
✓ test_obligation_events.py
```

**Implementação**:

```python
# routes/obligations.py
@router.get("/{obligation_id}/events", response_model=List[ObligationEventResponse])
async def get_obligation_events(
    obligation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get timeline of events for an obligation"""

    result = await db.execute(
        select(ObligationEvent)
        .where(ObligationEvent.obligation_id == obligation_id)
        .order_by(ObligationEvent.created_at.desc())
    )
    events = result.scalars().all()

    return events
```

**Critérios de Aceite**:
- Endpoint retorna eventos ordenados
- Testes passam

---

### Bloco 4.9: WebSocket Client (Frontend)

**Duração**: 3-4 horas
**Dependências**: Bloco 4.3

**Objetivos**:
- Cliente WebSocket React
- Auto-reconnect
- Event handlers
- Hook useWebSocket

**Entregáveis**:
```
apps/web/src/lib/ws/
✓ client.ts
✓ events.ts

apps/web/src/hooks/
✓ useWebSocket.ts
✓ useNotifications.ts

apps/web/app/(dashboard)/
✓ layout.tsx (atualizado com WebSocketProvider)
```

**Implementação**:

```typescript
// lib/ws/client.ts
export class WebSocketClient {
  private ws: WebSocket | null = null;
  private token: string;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

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
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      setTimeout(() => this.connect(), delay);
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

  send(message: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  disconnect() {
    this.ws?.close();
  }
}

// hooks/useWebSocket.ts
export function useWebSocket() {
  const { user, accessToken } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const clientRef = useRef<WebSocketClient | null>(null);

  useEffect(() => {
    if (!accessToken) return;

    const client = new WebSocketClient(accessToken);
    clientRef.current = client;

    client.on('connected', () => setIsConnected(true));
    client.on('disconnected', () => setIsConnected(false));

    client.connect();

    return () => {
      client.disconnect();
    };
  }, [accessToken]);

  const subscribe = useCallback((eventType: string, callback: (data: any) => void) => {
    clientRef.current?.on(eventType, callback);
  }, []);

  const unsubscribe = useCallback((eventType: string, callback: (data: any) => void) => {
    clientRef.current?.off(eventType, callback);
  }, []);

  return { isConnected, subscribe, unsubscribe };
}

// hooks/useNotifications.ts
export function useNotifications() {
  const { subscribe, unsubscribe } = useWebSocket();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const handler = (data: Notification) => {
      setNotifications(prev => [data, ...prev]);
      setUnreadCount(prev => prev + 1);

      // Show toast
      toast.info(data.title, {
        description: data.message,
      });
    };

    subscribe('notification', handler);

    return () => {
      unsubscribe('notification', handler);
    };
  }, [subscribe, unsubscribe]);

  const markAsRead = async (notificationId: string) => {
    await apiClient.patch(`/notifications/${notificationId}/read`);
    setNotifications(prev =>
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = async () => {
    await apiClient.post('/notifications/mark-all-read');
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    setUnreadCount(0);
  };

  return { notifications, unreadCount, markAsRead, markAllAsRead };
}
```

**Critérios de Aceite**:
- WebSocket conecta e reconecta
- Events são recebidos
- Hook funciona corretamente
- Toast mostra notificações

---

### Bloco 4.10: Notification Center UI

**Duração**: 4-5 horas
**Dependências**: Bloco 4.9

**Objetivos**:
- Bell icon com badge no header
- Dropdown com lista de notificações
- Marcar como lida
- Link para página completa

**Entregáveis**:
```
apps/web/src/components/ui/
✓ NotificationBell.tsx

apps/web/src/components/features/notifications/
✓ NotificationDropdown.tsx
✓ NotificationList.tsx
✓ NotificationItem.tsx

apps/web/app/(dashboard)/
✓ layout.tsx (atualizado com bell)

apps/web/app/(dashboard)/notificacoes/
✓ page.tsx
```

**Implementação**:

```typescript
// components/ui/NotificationBell.tsx
import { Bell } from 'lucide-react';
import { Badge, Button, Popover, PopoverTrigger, PopoverContent } from '@/heroui';
import { NotificationDropdown } from '@/components/features/notifications/NotificationDropdown';
import { useNotifications } from '@/hooks/useNotifications';

export function NotificationBell() {
  const { unreadCount } = useNotifications();

  return (
    <Popover placement="bottom-end">
      <PopoverTrigger>
        <Button
          isIconOnly
          variant="light"
          aria-label="Notificações"
        >
          <div className="relative">
            <Bell className="h-5 w-5" />
            {unreadCount > 0 && (
              <Badge
                content={unreadCount > 99 ? '99+' : unreadCount}
                color="danger"
                size="sm"
                className="absolute -top-1 -right-1"
              />
            )}
          </div>
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0">
        <NotificationDropdown />
      </PopoverContent>
    </Popover>
  );
}

// components/features/notifications/NotificationDropdown.tsx
export function NotificationDropdown() {
  const { notifications, markAsRead, markAllAsRead } = useNotifications();
  const recentNotifications = notifications.slice(0, 5);

  return (
    <div className="flex flex-col">
      <div className="flex items-center justify-between p-4 border-b">
        <h3 className="font-semibold">Notificações</h3>
        {notifications.some(n => !n.read) && (
          <Button
            size="sm"
            variant="light"
            onClick={markAllAsRead}
          >
            Marcar todas como lidas
          </Button>
        )}
      </div>

      <div className="max-h-96 overflow-y-auto">
        {recentNotifications.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            Nenhuma notificação
          </div>
        ) : (
          <NotificationList
            notifications={recentNotifications}
            onMarkAsRead={markAsRead}
          />
        )}
      </div>

      {notifications.length > 5 && (
        <div className="p-4 border-t">
          <Button
            as={Link}
            href="/notificacoes"
            variant="light"
            fullWidth
          >
            Ver todas
          </Button>
        </div>
      )}
    </div>
  );
}

// components/features/notifications/NotificationItem.tsx
export function NotificationItem({ notification, onMarkAsRead }: Props) {
  const handleClick = () => {
    if (!notification.read) {
      onMarkAsRead(notification.id);
    }
    if (notification.link) {
      router.push(notification.link);
    }
  };

  return (
    <div
      className={cn(
        "p-4 border-b cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition",
        !notification.read && "bg-blue-50/50 dark:bg-blue-950/20"
      )}
      onClick={handleClick}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          {getNotificationIcon(notification.type)}
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm">{notification.title}</p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {notification.message}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            {formatDistanceToNow(new Date(notification.created_at), {
              addSuffix: true,
              locale: ptBR
            })}
          </p>
        </div>
        {!notification.read && (
          <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 mt-1" />
        )}
      </div>
    </div>
  );
}

// app/(dashboard)/layout.tsx (atualizar header)
export default function DashboardLayout({ children }: Props) {
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="flex items-center justify-between px-6 py-4">
          <Logo />

          <div className="flex items-center gap-4">
            <NotificationBell />
            <UserMenu />
          </div>
        </div>
      </header>

      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

**Critérios de Aceite**:
- Bell icon aparece no header
- Badge mostra contagem correta
- Dropdown abre e fecha
- Notificações aparecem em tempo real
- Marcar como lida funciona
- Link para página completa funciona

---

### Bloco 4.11: Interface de Obrigações

**Duração**: 5-6 horas
**Dependências**: Blocos 4.8, 4.10

**Objetivos**:
- Página de obrigações
- Tabela com filtros
- Modal de detalhes
- Upload de comprovante
- Timeline de eventos

**Entregáveis**:
```
apps/web/app/(dashboard)/obrigacoes/
✓ page.tsx

apps/web/src/components/features/obrigacoes/
✓ ObligationsTable.tsx
✓ ObligationFilters.tsx
✓ ObligationCard.tsx
✓ ObligationTimeline.tsx
✓ ReceiptUploadModal.tsx

apps/web/src/hooks/
✓ useObligations.ts

apps/web/src/lib/api/endpoints/
✓ obligations.ts
```

**Implementação**: (Detalhes completos serão implementados no bloco)

**Critérios de Aceite**:
- Tabela mostra obrigações
- Filtros funcionam (status, cliente, período)
- Modal abre com detalhes
- Upload de comprovante funciona
- Timeline mostra eventos
- Status muda para concluída após upload

---

### Bloco 4.12: Portal do Cliente

**Duração**: 3-4 horas
**Dependências**: Bloco 4.11

**Objetivos**:
- Página de obrigações no portal
- Visualização somente leitura
- Filtros limitados

**Entregáveis**:
```
apps/web/app/(portal)/obrigacoes/
✓ page.tsx

apps/web/src/components/features/portal/
✓ ObligationsView.tsx
```

**Critérios de Aceite**:
- Cliente vê apenas suas obrigações
- Não pode editar/excluir
- Interface simplificada

---

## 📋 Checklist de Validação do Marco 4

Após completar todos os blocos:

```bash
# 1. Lint
pnpm lint

# 2. Type-check
pnpm type-check

# 3. Testes backend
cd apps/api
venv/Scripts/pytest.exe -v --cov=app --cov-report=term-missing

# 4. Testes frontend (se houver)
cd apps/web
pnpm test

# 5. Build
pnpm build

# 6. Docker compose
docker compose up -d

# 7. Testar manualmente:
# - Gerar obrigações para próximo mês
# - Fazer upload de comprovante
# - Verificar notificação em tempo real
# - Testar WebSocket (desconectar/reconectar)
# - Portal do cliente
```

---

## 🎯 Resultado Esperado

Ao final do Marco 4, teremos:

### Backend
- ✅ 4 novos models (Obligation, ObligationType, ObligationEvent, Notification)
- ✅ WebSocket infrastructure completa
- ✅ Strategy pattern com 4 strategies
- ✅ Factory de obrigações
- ✅ 15+ endpoints RESTful
- ✅ Geração automática de obrigações
- ✅ Processo de baixa com upload
- ✅ Notificações em tempo real
- ✅ 30+ testes (cobertura 70%+)

### Frontend
- ✅ WebSocket client com auto-reconnect
- ✅ Notification bell no header
- ✅ Notification center completo
- ✅ Página de obrigações
- ✅ Upload de comprovantes
- ✅ Timeline de eventos
- ✅ Portal do cliente
- ✅ Toasts em tempo real

### Funcionalidades
- ✅ Gerar obrigações mensais com um clique
- ✅ Completar obrigação com upload obrigatório
- ✅ Receber notificações em tempo real
- ✅ Ver histórico completo (timeline)
- ✅ Filtros avançados
- ✅ Dashboard com métricas

---

_Criado em: 2025-10-30_
_Marco: 4 - Obrigações + Notificações_
_Status: Planejamento Completo_
