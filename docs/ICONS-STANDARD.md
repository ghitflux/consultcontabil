# Padrão de Ícones - ContabilConsult

## 📋 Visão Geral

Este documento define o padrão de uso de ícones no projeto ContabilConsult. Todos os ícones devem ser importados da biblioteca **lucide-react** através do barrel export centralizado.

## 🎯 Regras Obrigatórias

### 1. Import Centralizado

**SEMPRE** importe ícones de `@/lib/icons`, **NUNCA** diretamente de `lucide-react`:

```tsx
// ✅ CORRETO
import { CheckIcon, CopyIcon, UserIcon } from '@/lib/icons';

// ❌ ERRADO
import { Check, Copy, User } from 'lucide-react';
```

### 2. Nomenclatura

Todos os ícones devem ter o sufixo `Icon`:

```tsx
// ✅ CORRETO
import { CheckIcon } from '@/lib/icons';
<CheckIcon className="h-4 w-4" />

// ❌ ERRADO
import { Check } from 'lucide-react';
<Check className="h-4 w-4" />
```

### 3. Tamanhos Padrão

Use as classes Tailwind para tamanhos consistentes:

```tsx
// Tamanhos disponíveis
<Icon className="h-3 w-3" />  // Extra small (12px)
<Icon className="h-4 w-4" />  // Small (16px) - default para botões
<Icon className="h-5 w-5" />  // Medium (20px) - default geral
<Icon className="h-6 w-6" />  // Large (24px)
<Icon className="h-8 w-8" />  // Extra large (32px)
```

### 4. Props Comuns

Os ícones lucide-react aceitam props padrão de SVG:

```tsx
<CheckIcon
  className="h-5 w-5"
  color="currentColor"
  strokeWidth={2}
/>
```

## 📦 Ícones Disponíveis

### Ações
- `CheckIcon` - Confirmação, sucesso
- `CopyIcon` - Copiar texto/dados
- `DownloadIcon` - Download de arquivos
- `UploadIcon` - Upload de arquivos
- `SaveIcon` - Salvar dados
- `EditIcon` - Edição
- `TrashIcon` - Exclusão
- `PlusIcon` - Adicionar
- `MinusIcon` - Remover
- `XIcon` - Fechar/Cancelar
- `MoreVerticalIcon` - Menu vertical
- `MoreHorizontalIcon` - Menu horizontal

### Navegação
- `ChevronLeftIcon`, `ChevronRightIcon`, `ChevronDownIcon`, `ChevronUpIcon`
- `ArrowLeftIcon`, `ArrowRightIcon`
- `MenuIcon` - Menu hamburguer
- `HomeIcon` - Página inicial

### Status
- `AlertCircleIcon` - Informação importante
- `AlertTriangleIcon` - Aviso
- `CheckCircleIcon` - Sucesso
- `XCircleIcon` - Erro
- `InfoIcon` - Informação

### Arquivos & Documentos
- `FileIcon` - Arquivo genérico
- `FileTextIcon` - Documento de texto
- `FilePlusIcon` - Novo arquivo
- `FolderIcon`, `FolderOpenIcon`
- `PaperclipIcon` - Anexo

### Negócio
- `UsersIcon`, `UserIcon`, `UserPlusIcon`
- `BuildingIcon`, `Building2Icon`
- `BriefcaseIcon`
- `CalendarIcon`, `ClockIcon`

### Financeiro
- `DollarSignIcon` - Moeda
- `TrendingUpIcon`, `TrendingDownIcon` - Tendências
- `CreditCardIcon` - Pagamento
- `ReceiptIcon` - Recibo
- `WalletIcon` - Carteira

### Comunicação
- `MailIcon` - Email
- `SendIcon` - Enviar
- `MessageSquareIcon` - Mensagem
- `BellIcon`, `BellRingIcon` - Notificações

### Dados & Relatórios
- `BarChartIcon`, `LineChartIcon`, `PieChartIcon`
- `TableIcon` - Tabela
- `FileSpreadsheetIcon` - Planilha
- `FilterIcon` - Filtro
- `SearchIcon` - Busca

### Configurações
- `SettingsIcon` - Configurações
- `SlidersIcon` - Ajustes
- `EyeIcon`, `EyeOffIcon` - Visibilidade
- `LockIcon`, `UnlockIcon` - Segurança

### Interface
- `LoaderIcon` - Carregamento (com animação spin)
- `RefreshIcon` - Atualizar
- `ExternalLinkIcon` - Link externo
- `LinkIcon` - Link
- `MaximizeIcon`, `MinimizeIcon`

### Específicos do Domínio
- `ObligationIcon` - Obrigações fiscais
- `LicenseIcon` - Licenças
- `TransactionIcon` - Transações
- `ReportIcon` - Relatórios

## 🎨 Exemplos de Uso

### Botão com Ícone

```tsx
import { PlusIcon } from '@/lib/icons';
import { Button } from '@/heroui';

<Button>
  <PlusIcon className="h-4 w-4 mr-2" />
  Adicionar Cliente
</Button>
```

### Ícone de Loading

```tsx
import { LoaderIcon } from '@/lib/icons';

<LoaderIcon className="h-5 w-5 animate-spin" />
```

### Ícone em Tooltip

```tsx
import { InfoIcon } from '@/lib/icons';
import { Tooltip } from '@/heroui';

<Tooltip content="Informação adicional">
  <InfoIcon className="h-4 w-4 text-gray-400" />
</Tooltip>
```

### Ícone Condicional

```tsx
import { CheckIcon, XIcon } from '@/lib/icons';

{isSuccess ? (
  <CheckIcon className="h-5 w-5 text-success" />
) : (
  <XIcon className="h-5 w-5 text-danger" />
)}
```

## 🔧 Adicionar Novo Ícone

Se precisar de um ícone que não está na lista:

1. Encontre o ícone em [lucide.dev](https://lucide.dev)
2. Adicione a exportação em `apps/web/src/lib/icons.ts`:

```ts
export {
  // ... outros ícones
  NomeDoIcone as NomeDoIconeIcon,
} from 'lucide-react';
```

3. Documente neste arquivo

## ❌ O Que NÃO Fazer

### 1. Não usar SVG inline

```tsx
// ❌ ERRADO
<svg xmlns="http://www.w3.org/2000/svg">
  <path d="..." />
</svg>

// ✅ CORRETO
import { CheckIcon } from '@/lib/icons';
<CheckIcon className="h-4 w-4" />
```

### 2. Não misturar bibliotecas

```tsx
// ❌ ERRADO
import { FaCheck } from 'react-icons/fa';
import { CheckIcon } from '@/lib/icons';

// ✅ CORRETO
import { CheckIcon } from '@/lib/icons';
```

### 3. Não usar @heroui/icons

```tsx
// ❌ ERRADO
import { CheckIcon } from '@heroui/icons';

// ✅ CORRETO
import { CheckIcon } from '@/lib/icons';
```

### 4. Não usar emojis como ícones

```tsx
// ❌ EVITAR (exceto em casos específicos)
<span>✅</span>

// ✅ PREFERIR
import { CheckCircleIcon } from '@/lib/icons';
<CheckCircleIcon className="h-5 w-5" />
```

## 📱 Responsividade

Use classes Tailwind responsivas quando necessário:

```tsx
<Icon className="h-4 w-4 md:h-5 md:w-5 lg:h-6 lg:w-6" />
```

## ♿ Acessibilidade

Para ícones decorativos:

```tsx
<CheckIcon className="h-4 w-4" aria-hidden="true" />
```

Para ícones informativos, adicione texto alternativo:

```tsx
<span>
  <CheckIcon className="h-4 w-4" />
  <span className="sr-only">Confirmado</span>
</span>
```

## 🎯 Performance

Lucide-react é tree-shakeable - apenas os ícones importados serão incluídos no bundle final. Por isso, não há problema em ter muitos ícones disponíveis em `@/lib/icons`.

## 🔄 Migração de Código Legado

Ao encontrar código com SVG inline ou outros ícones:

1. Identifique o ícone equivalente em lucide-react
2. Substitua pelo import de `@/lib/icons`
3. Ajuste classes CSS se necessário

## 📚 Recursos

- [Lucide Icons Gallery](https://lucide.dev/icons/)
- [Lucide React Docs](https://lucide.dev/guide/packages/lucide-react)

---

**Última atualização**: 2025-10-31
**Versão**: 1.0.0
