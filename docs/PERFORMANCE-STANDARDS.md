# Padrões de Performance - ContabilConsult

## 📋 Visão Geral

Este documento define as práticas e padrões de performance para o projeto ContabilConsult. Seguir estas diretrizes garante uma aplicação rápida e eficiente.

## 🎯 Princípios Fundamentais

1. **Lazy Loading First**: Carregue componentes e dados apenas quando necessário
2. **Memoization Estratégica**: Use React.memo e hooks de memoization onde apropriado
3. **Code Splitting**: Divida o bundle em chunks menores
4. **Otimização de Imagens**: Use Next.js Image e formatos modernos
5. **Cache Inteligente**: Implemente caching de dados e assets

## 🚀 Next.js Performance

### 1. App Router e Server Components

Use Server Components por padrão, Client Components apenas quando necessário:

```tsx
// ✅ CORRETO - Server Component (default)
// app/clientes/page.tsx
export default async function ClientesPage() {
  const data = await fetchClientes();
  return <ClientesTable data={data} />;
}

// ✅ CORRETO - Client Component quando necessário
// components/ClientesTable.tsx
'use client';
import { useState } from 'react';

export function ClientesTable({ data }) {
  const [filter, setFilter] = useState('');
  // ...
}
```

### 2. Dynamic Imports

Use dynamic imports para componentes pesados:

```tsx
// ✅ CORRETO - Modal pesado carregado sob demanda
import dynamic from 'next/dynamic';

const ReportBuilderModal = dynamic(
  () => import('@/components/features/relatorios/ReportBuilder'),
  {
    loading: () => <LoadingSpinner />,
    ssr: false, // Se não precisa de SSR
  }
);
```

### 3. Route Segment Config

Configure opções de performance por rota:

```tsx
// app/relatorios/page.tsx
export const dynamic = 'force-dynamic'; // Para dados em tempo real
export const revalidate = 3600; // Cache por 1 hora

export default async function RelatoriosPage() {
  // ...
}
```

## ⚛️ React Performance

### 1. React.memo

Use para componentes que renderizam frequentemente com as mesmas props:

```tsx
import { memo } from 'react';

// ✅ CORRETO
export const ClientCard = memo(function ClientCard({ client }) {
  return (
    <Card>
      <h3>{client.nome}</h3>
      <p>{client.cnpj}</p>
    </Card>
  );
});
```

### 2. useMemo

Use para cálculos custosos:

```tsx
import { useMemo } from 'react';

export function RevenueChart({ transactions }) {
  // ✅ CORRETO - Cálculo só refaz quando transactions mudam
  const chartData = useMemo(() => {
    return transactions.reduce((acc, t) => {
      // cálculo complexo...
      return acc;
    }, []);
  }, [transactions]);

  return <Chart data={chartData} />;
}
```

### 3. useCallback

Use para funções passadas como props:

```tsx
import { useCallback } from 'react';

export function ClientsTable({ clients, onDelete }) {
  // ✅ CORRETO - Função estável
  const handleDelete = useCallback((id: string) => {
    onDelete(id);
  }, [onDelete]);

  return (
    <Table>
      {clients.map(client => (
        <ClientRow key={client.id} client={client} onDelete={handleDelete} />
      ))}
    </Table>
  );
}
```

### 4. Keys Eficientes

Use IDs estáveis como keys:

```tsx
// ✅ CORRETO
{clients.map(client => (
  <ClientRow key={client.id} client={client} />
))}

// ❌ ERRADO
{clients.map((client, index) => (
  <ClientRow key={index} client={client} />
))}
```

## 📦 Bundle Optimization

### 1. Barrel Exports

Evite barrel exports que importam tudo:

```tsx
// ❌ ERRADO - Importa tudo mesmo usando só 1 função
export * from './utils/dates';
export * from './utils/format';
export * from './utils/validation';

// ✅ CORRETO - Imports específicos
export { formatDate } from './utils/dates';
export { formatCurrency } from './utils/format';
```

### 2. Tree Shaking

Importe apenas o necessário:

```tsx
// ✅ CORRETO
import { formatDate } from 'date-fns/formatDate';

// ❌ EVITAR (importa biblioteca inteira)
import { formatDate } from 'date-fns';
```

### 3. Code Splitting por Rota

Next.js faz automaticamente, mas você pode otimizar:

```tsx
// app/dashboard/relatorios/page.tsx
import { Suspense } from 'react';

export default function RelatoriosPage() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <ReportsDashboard />
    </Suspense>
  );
}
```

## 🖼️ Imagens

### 1. Next.js Image Component

**SEMPRE** use `next/image`:

```tsx
import Image from 'next/image';

// ✅ CORRETO
<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={50}
  priority // Para LCP (Largest Contentful Paint)
/>

// ❌ ERRADO
<img src="/logo.png" alt="Logo" />
```

### 2. Lazy Loading de Imagens

```tsx
<Image
  src={client.avatar}
  alt={client.nome}
  width={40}
  height={40}
  loading="lazy"
/>
```

## 📊 Data Fetching

### 1. Server-Side Fetching

Prefira buscar dados no servidor:

```tsx
// app/clientes/page.tsx
async function getClientes() {
  const res = await fetch('http://api:8000/api/v1/clients', {
    next: { revalidate: 60 }, // Cache por 60 segundos
  });
  return res.json();
}

export default async function ClientesPage() {
  const clientes = await getClientes();
  return <ClientesTable data={clientes} />;
}
```

### 2. Parallel Data Fetching

```tsx
// ✅ CORRETO - Paralelo
async function getData() {
  const [clients, obligations] = await Promise.all([
    fetchClients(),
    fetchObligations(),
  ]);
  return { clients, obligations };
}

// ❌ ERRADO - Sequencial
async function getData() {
  const clients = await fetchClients();
  const obligations = await fetchObligations();
  return { clients, obligations };
}
```

### 3. Pagination

Sempre implemente paginação para listas grandes:

```tsx
export function useClients(page = 1, size = 20) {
  return useSWR(`/clients?page=${page}&size=${size}`, fetcher);
}
```

## 🎨 Rendering Performance

### 1. Virtualization

Para listas com 100+ itens, use virtualização:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

export function VirtualizedList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px` }}>
        {rowVirtualizer.getVirtualItems().map(virtualRow => (
          <div key={virtualRow.index} data-index={virtualRow.index}>
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 2. Debounce em Inputs

```tsx
import { useMemo, useState } from 'react';

function debounce(fn: Function, ms: number) {
  let timer: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

export function SearchInput() {
  const [query, setQuery] = useState('');

  const debouncedSearch = useMemo(
    () => debounce((value: string) => {
      // Fazer busca
    }, 300),
    []
  );

  return (
    <input
      type="text"
      onChange={(e) => {
        setQuery(e.target.value);
        debouncedSearch(e.target.value);
      }}
    />
  );
}
```

### 3. Skeleton Loading

Prefira skeletons a spinners:

```tsx
export function ClientCard({ client, isLoading }) {
  if (isLoading) {
    return (
      <Card>
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-1/2 mt-2" />
      </Card>
    );
  }

  return (
    <Card>
      <h3>{client.nome}</h3>
      <p>{client.cnpj}</p>
    </Card>
  );
}
```

## 🔍 Monitoramento

### 1. Web Vitals

Next.js reporta automaticamente Core Web Vitals:

```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 2. Performance Budget

Metas do projeto:

- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **TTI** (Time to Interactive): < 3.5s
- **Bundle Size**: < 200KB (gzipped)

## 🛠️ Ferramentas

### 1. Lighthouse

```bash
# Rodar Lighthouse localmente
npx lighthouse http://localhost:3000 --view
```

### 2. Bundle Analyzer

```bash
# Analisar bundle
ANALYZE=true pnpm build
```

### 3. React DevTools Profiler

Use para identificar renderizações desnecessárias.

## ✅ Checklist de Performance

Antes de cada PR:

- [ ] Componentes pesados usam `React.memo`
- [ ] Modals/Drawers usam `dynamic import`
- [ ] Listas grandes têm paginação ou virtualização
- [ ] Inputs de busca têm debounce
- [ ] Imagens usam `next/image`
- [ ] Dados são buscados no servidor quando possível
- [ ] Cálculos custosos usam `useMemo`
- [ ] Callbacks usam `useCallback`
- [ ] Keys são IDs estáveis
- [ ] Não há re-renders desnecessários

## 🚫 Anti-Patterns

### 1. Estado Desnecessário

```tsx
// ❌ ERRADO
function Component({ items }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(items.length);
  }, [items]);

  return <p>Total: {count}</p>;
}

// ✅ CORRETO
function Component({ items }) {
  return <p>Total: {items.length}</p>;
}
```

### 2. Funções Inline em Props

```tsx
// ❌ ERRADO
<Button onClick={() => handleClick(id)}>Click</Button>

// ✅ CORRETO
const handleButtonClick = useCallback(() => handleClick(id), [id]);
<Button onClick={handleButtonClick}>Click</Button>
```

### 3. useEffect para Cálculos

```tsx
// ❌ ERRADO
const [total, setTotal] = useState(0);
useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.value, 0));
}, [items]);

// ✅ CORRETO
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.value, 0),
  [items]
);
```

## 📚 Recursos

- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [React Performance](https://react.dev/learn/render-and-commit)
- [Web.dev Performance](https://web.dev/performance/)
- [MDN Performance](https://developer.mozilla.org/en-US/docs/Web/Performance)

---

**Última atualização**: 2025-10-31
**Versão**: 1.0.0
