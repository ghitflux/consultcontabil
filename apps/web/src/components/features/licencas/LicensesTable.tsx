'use client';

import {
  Button,
  Chip,
  Spinner,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
  Tooltip,
} from '@/heroui';
import type { License } from '@/types/license';
import {
  LICENSE_STATUS_LABELS,
  LICENSE_TYPE_LABELS,
  formatExpirationStatus,
  getExpirationBadgeColor,
  getLicenseStatusColor,
} from '@/types/license';

interface LicensesTableProps {
  licenses: License[];
  loading?: boolean;
  onViewDetails?: (license: License) => void;
  onRenew?: (license: License) => void;
  onEdit?: (license: License) => void;
  onDelete?: (license: License) => void;
}

export function LicensesTable({
  licenses,
  loading,
  onViewDetails,
  onRenew,
  onEdit,
  onDelete,
}: LicensesTableProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Sem vencimento';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(date);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (licenses.length === 0) {
    return (
      <div className="text-center p-8 text-default-400">
        <p className="text-4xl mb-2">📜</p>
        <p>Nenhuma licença encontrada</p>
      </div>
    );
  }

  return (
    <Table aria-label="Tabela de licenças">
      <TableHeader>
        <TableColumn>CLIENTE</TableColumn>
        <TableColumn>TIPO</TableColumn>
        <TableColumn>REGISTRO</TableColumn>
        <TableColumn>ÓRGÃO EMISSOR</TableColumn>
        <TableColumn>VENCIMENTO</TableColumn>
        <TableColumn>STATUS</TableColumn>
        <TableColumn>AÇÕES</TableColumn>
      </TableHeader>
      <TableBody>
        {licenses.map((license) => (
          <TableRow key={license.id}>
            <TableCell>
              <div>
                <p className="font-semibold">{license.client_name || 'N/A'}</p>
                <p className="text-xs text-default-400">{license.client_id}</p>
              </div>
            </TableCell>
            <TableCell>
              <p className="font-medium">{LICENSE_TYPE_LABELS[license.license_type]}</p>
            </TableCell>
            <TableCell>
              <p className="font-mono text-sm">{license.registration_number}</p>
            </TableCell>
            <TableCell>
              <p className="text-sm">{license.issuing_authority}</p>
            </TableCell>
            <TableCell>
              <div>
                <p
                  className={
                    license.is_expired
                      ? 'text-danger font-semibold'
                      : license.is_expiring_soon
                        ? 'text-warning font-semibold'
                        : ''
                  }
                >
                  {formatDate(license.expiration_date)}
                </p>
                {license.expiration_date && (
                  <p className="text-xs text-default-400">{formatExpirationStatus(license)}</p>
                )}
              </div>
            </TableCell>
            <TableCell>
              <div className="flex flex-col gap-1">
                <Chip color={getLicenseStatusColor(license.status) as any} size="sm" variant="flat">
                  {LICENSE_STATUS_LABELS[license.status]}
                </Chip>
                {license.is_expiring_soon && !license.is_expired && (
                  <Chip color={getExpirationBadgeColor(license) as any} size="sm" variant="flat">
                    Vence em {license.days_until_expiration} dias
                  </Chip>
                )}
                {license.is_expired && (
                  <Chip color="danger" size="sm" variant="flat">
                    Vencida
                  </Chip>
                )}
              </div>
            </TableCell>
            <TableCell>
              <div className="flex gap-2">
                {onViewDetails && (
                  <Tooltip content="Ver detalhes">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      onPress={() => onViewDetails(license)}
                    >
                      👁️
                    </Button>
                  </Tooltip>
                )}
                {onRenew && license.status !== 'cancelada' && (
                  <Tooltip content="Renovar">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="success"
                      onPress={() => onRenew(license)}
                    >
                      🔄
                    </Button>
                  </Tooltip>
                )}
                {onEdit && license.status !== 'cancelada' && (
                  <Tooltip content="Editar">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="primary"
                      onPress={() => onEdit(license)}
                    >
                      ✏️
                    </Button>
                  </Tooltip>
                )}
                {onDelete && (
                  <Tooltip content="Excluir">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="danger"
                      onPress={() => onDelete(license)}
                    >
                      🗑️
                    </Button>
                  </Tooltip>
                )}
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
