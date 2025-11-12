"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Button,
  Input,
  Select,
  SelectItem,
  Pagination,
  Spinner,
  Tooltip,
  useDisclosure,
} from "@heroui/react";
import { SearchIcon, PlusIcon, EditIcon, KeyIcon, TrashIcon } from "@/lib/icons";
import { UserRoleChip, UserStatusChip } from "./UserChips";
import { useUsers } from "@/hooks/useUsers";
import type { UserListItem, UserRole } from "@/types/user";
import { getRoleLabel } from "@/types/user";
import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";

interface UsersTableProps {
  onEdit: (user: UserListItem) => void;
  onResetPassword: (user: UserListItem) => void;
  onCreateNew: () => void;
}

export function UsersTable({ onEdit, onResetPassword, onCreateNew }: UsersTableProps) {
  const { users, isLoading, error, fetchUsers, deleteUser, activateUser, deactivateUser } = useUsers();

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState<UserRole | "">("");
  const [statusFilter, setStatusFilter] = useState<boolean | undefined>(undefined);
  const [page, setPage] = useState(1);
  const pageSize = 10;

  // Load users
  const loadUsers = useCallback(() => {
    fetchUsers({
      query: searchQuery || undefined,
      role: roleFilter || undefined,
      is_active: statusFilter,
      page,
      size: pageSize,
    });
  }, [searchQuery, roleFilter, statusFilter, page, fetchUsers]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  // Handlers
  const handleToggleStatus = async (user: UserListItem) => {
    try {
      if (user.is_active) {
        await deactivateUser(user.id);
      } else {
        await activateUser(user.id);
      }
    } catch (error) {
      console.error("Erro ao alterar status:", error);
    }
  };

  const handleDelete = async (user: UserListItem) => {
    if (!confirm(`Tem certeza que deseja excluir o usuário "${user.name}"?`)) {
      return;
    }

    try {
      await deleteUser(user.id);
    } catch (error) {
      console.error("Erro ao excluir usuário:", error);
    }
  };

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
    setPage(1); // Reset to first page
  };

  const handleRoleFilterChange = (value: string) => {
    setRoleFilter(value as UserRole | "");
    setPage(1);
  };

  const handleStatusFilterChange = (value: string) => {
    if (value === "all") {
      setStatusFilter(undefined);
    } else {
      setStatusFilter(value === "active");
    }
    setPage(1);
  };

  // Render helpers
  const renderLastLogin = (lastLogin: string | null) => {
    if (!lastLogin) return <span className="text-default-400">Nunca</span>;

    try {
      return (
        <span className="text-sm text-default-600">
          {formatDistanceToNow(new Date(lastLogin), {
            addSuffix: true,
            locale: ptBR,
          })}
        </span>
      );
    } catch {
      return <span className="text-default-400">-</span>;
    }
  };

  const columns = [
    { key: "name", label: "NOME" },
    { key: "email", label: "EMAIL" },
    { key: "role", label: "PERFIL" },
    { key: "status", label: "STATUS" },
    { key: "last_login", label: "ÚLTIMO ACESSO" },
    { key: "actions", label: "AÇÕES" },
  ];

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div className="flex flex-col gap-3 md:flex-row md:items-end">
          {/* Search */}
          <Input
            isClearable
            placeholder="Buscar por nome ou email..."
            startContent={<SearchIcon className="text-default-400" />}
            value={searchQuery}
            onValueChange={handleSearchChange}
            className="w-full md:w-64"
          />

          {/* Role filter */}
          <Select
            placeholder="Todos os perfis"
            selectedKeys={roleFilter ? [roleFilter] : []}
            onChange={(e) => handleRoleFilterChange(e.target.value)}
            className="w-full md:w-48"
          >
            <SelectItem key="" value="">
              Todos os perfis
            </SelectItem>
            <SelectItem key="admin" value="admin">
              {getRoleLabel("admin" as UserRole)}
            </SelectItem>
            <SelectItem key="func" value="func">
              {getRoleLabel("func" as UserRole)}
            </SelectItem>
            <SelectItem key="cliente" value="cliente">
              {getRoleLabel("cliente" as UserRole)}
            </SelectItem>
          </Select>

          {/* Status filter */}
          <Select
            placeholder="Todos os status"
            selectedKeys={statusFilter === undefined ? ["all"] : statusFilter ? ["active"] : ["inactive"]}
            onChange={(e) => handleStatusFilterChange(e.target.value)}
            className="w-full md:w-40"
          >
            <SelectItem key="all" value="all">
              Todos
            </SelectItem>
            <SelectItem key="active" value="active">
              Ativos
            </SelectItem>
            <SelectItem key="inactive" value="inactive">
              Inativos
            </SelectItem>
          </Select>
        </div>

        {/* Create button */}
        <Button color="primary" startContent={<PlusIcon />} onPress={onCreateNew}>
          Novo Usuário
        </Button>
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg bg-danger-50 p-4 text-danger">
          <p className="font-semibold">Erro ao carregar usuários</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Table */}
      <Table
        aria-label="Tabela de usuários"
        bottomContent={
          users && users.pages > 1 ? (
            <div className="flex w-full justify-center">
              <Pagination
                isCompact
                showControls
                showShadow
                color="primary"
                page={page}
                total={users.pages}
                onChange={setPage}
              />
            </div>
          ) : null
        }
      >
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key} align={column.key === "actions" ? "center" : "start"}>
              {column.label}
            </TableColumn>
          )}
        </TableHeader>
        <TableBody
          items={users?.items || []}
          isLoading={isLoading}
          loadingContent={<Spinner label="Carregando usuários..." />}
          emptyContent={
            <div className="py-8 text-center">
              <p className="text-lg font-semibold text-default-600">Nenhum usuário encontrado</p>
              <p className="text-sm text-default-400">
                {searchQuery || roleFilter || statusFilter !== undefined
                  ? "Tente ajustar os filtros"
                  : "Clique em 'Novo Usuário' para criar o primeiro"}
              </p>
            </div>
          }
        >
          {(item) => (
            <TableRow key={item.id}>
              <TableCell>
                <div className="flex flex-col">
                  <span className="font-semibold">{item.name}</span>
                </div>
              </TableCell>
              <TableCell>
                <span className="text-sm text-default-600">{item.email}</span>
              </TableCell>
              <TableCell>
                <UserRoleChip role={item.role} />
              </TableCell>
              <TableCell>
                <UserStatusChip isActive={item.is_active} />
              </TableCell>
              <TableCell>{renderLastLogin(item.last_login_at)}</TableCell>
              <TableCell>
                <div className="flex items-center justify-center gap-2">
                  <Tooltip content="Editar">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      onPress={() => onEdit(item)}
                      aria-label="Editar usuário"
                    >
                      <EditIcon className="h-4 w-4" />
                    </Button>
                  </Tooltip>

                  <Tooltip content={item.is_active ? "Desativar" : "Ativar"}>
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color={item.is_active ? "warning" : "success"}
                      onPress={() => handleToggleStatus(item)}
                      aria-label={item.is_active ? "Desativar usuário" : "Ativar usuário"}
                    >
                      <span className="text-sm font-semibold">
                        {item.is_active ? "🔒" : "🔓"}
                      </span>
                    </Button>
                  </Tooltip>

                  <Tooltip content="Resetar senha">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="secondary"
                      onPress={() => onResetPassword(item)}
                      aria-label="Resetar senha"
                    >
                      <KeyIcon className="h-4 w-4" />
                    </Button>
                  </Tooltip>

                  <Tooltip content="Excluir" color="danger">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="danger"
                      onPress={() => handleDelete(item)}
                      aria-label="Excluir usuário"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </Button>
                  </Tooltip>
                </div>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>

      {/* Footer info */}
      {users && (
        <div className="flex items-center justify-between text-sm text-default-500">
          <p>
            Mostrando {(page - 1) * pageSize + 1} a {Math.min(page * pageSize, users.total)} de{" "}
            {users.total} usuários
          </p>
          <p>Página {page} de {users.pages}</p>
        </div>
      )}
    </div>
  );
}
