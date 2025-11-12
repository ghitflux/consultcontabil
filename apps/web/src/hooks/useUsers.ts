/**
 * Hook for managing users state and operations.
 */

import { usersApi, type UserFilters } from "@/lib/api/endpoints/users";
import type {
  User,
  UserCreate,
  UserUpdate,
  PaginatedUsersResponse,
  UserResetPasswordRequest,
  UserResetPasswordResponse,
} from "@/types/user";
import { useCallback, useState } from "react";

export function useUsers() {
  const [users, setUsers] = useState<PaginatedUsersResponse | null>(null);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async (filters?: UserFilters) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await usersApi.list(filters);
      setUsers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao carregar usuários");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchUserById = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await usersApi.getById(id);
      setSelectedUser(data);
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao carregar usuário");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createUser = useCallback(
    async (data: UserCreate) => {
      setIsLoading(true);
      setError(null);

      try {
        const newUser = await usersApi.create(data);
        // Refresh list
        if (users) {
          await fetchUsers({
            page: users.page,
            size: users.size,
          });
        }
        return newUser;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao criar usuário");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [users, fetchUsers]
  );

  const updateUser = useCallback(
    async (id: string, data: UserUpdate) => {
      setIsLoading(true);
      setError(null);

      try {
        const updatedUser = await usersApi.update(id, data);
        // Refresh list
        if (users) {
          await fetchUsers({
            page: users.page,
            size: users.size,
          });
        }
        // Update selected user if it's the one being edited
        if (selectedUser?.id === id) {
          setSelectedUser(updatedUser);
        }
        return updatedUser;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao atualizar usuário");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [users, selectedUser, fetchUsers]
  );

  const deleteUser = useCallback(
    async (id: string) => {
      setIsLoading(true);
      setError(null);

      try {
        await usersApi.delete(id);
        // Refresh list
        if (users) {
          await fetchUsers({
            page: users.page,
            size: users.size,
          });
        }
        // Clear selected user if it's the one being deleted
        if (selectedUser?.id === id) {
          setSelectedUser(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao excluir usuário");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [users, selectedUser, fetchUsers]
  );

  const activateUser = useCallback(
    async (id: string) => {
      setIsLoading(true);
      setError(null);

      try {
        await usersApi.activate(id);
        // Refresh list
        if (users) {
          await fetchUsers({
            page: users.page,
            size: users.size,
          });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao ativar usuário");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [users, fetchUsers]
  );

  const deactivateUser = useCallback(
    async (id: string) => {
      setIsLoading(true);
      setError(null);

      try {
        await usersApi.deactivate(id);
        // Refresh list
        if (users) {
          await fetchUsers({
            page: users.page,
            size: users.size,
          });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao desativar usuário");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [users, fetchUsers]
  );

  const resetPassword = useCallback(
    async (id: string, data: UserResetPasswordRequest): Promise<UserResetPasswordResponse> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await usersApi.resetPassword(id, data);
        return response;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Falha ao resetar senha");
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  return {
    users,
    selectedUser,
    isLoading,
    error,
    fetchUsers,
    fetchUserById,
    createUser,
    updateUser,
    deleteUser,
    activateUser,
    deactivateUser,
    resetPassword,
    setSelectedUser,
  };
}
