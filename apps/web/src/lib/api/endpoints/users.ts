/**
 * Users API endpoints
 */

import { apiClient } from "../client";
import type {
  User,
  UserCreate,
  UserUpdate,
  UserListItem,
  PaginatedUsersResponse,
  UserResetPasswordRequest,
  UserResetPasswordResponse,
  UserRole,
} from "@/types/user";

export interface UserFilters {
  query?: string;
  role?: UserRole | "";
  is_active?: boolean;
  page?: number;
  size?: number;
}

export const usersApi = {
  /**
   * List all users with optional filters (Admin only)
   */
  async list(filters?: UserFilters): Promise<PaginatedUsersResponse> {
    const params = new URLSearchParams();

    if (filters?.query) params.append("query", filters.query);
    if (filters?.role && filters.role !== "") params.append("role", filters.role);
    if (filters?.is_active !== undefined) params.append("is_active", filters.is_active.toString());
    if (filters?.page) params.append("page", filters.page.toString());
    if (filters?.size) params.append("size", filters.size.toString());

    const queryString = params.toString();
    const endpoint = queryString ? `/users?${queryString}` : "/users";

    return apiClient.get<PaginatedUsersResponse>(endpoint);
  },

  /**
   * Get current user info
   */
  async me(): Promise<User> {
    return apiClient.get<User>("/users/me");
  },

  /**
   * Get a user by ID (Admin or Func only)
   */
  async getById(id: string): Promise<User> {
    return apiClient.get<User>(`/users/${id}`);
  },

  /**
   * Create a new user (Admin only)
   */
  async create(data: UserCreate): Promise<User> {
    return apiClient.post<User>("/users", data);
  },

  /**
   * Update a user (Admin or self)
   */
  async update(id: string, data: UserUpdate): Promise<User> {
    return apiClient.put<User>(`/users/${id}`, data);
  },

  /**
   * Delete a user (Admin only)
   */
  async delete(id: string): Promise<{ success: boolean; message: string }> {
    return apiClient.delete<{ success: boolean; message: string }>(`/users/${id}`);
  },

  /**
   * Activate a user (Admin only)
   */
  async activate(id: string): Promise<{ success: boolean; message: string }> {
    return apiClient.patch<{ success: boolean; message: string }>(`/users/${id}/activate`);
  },

  /**
   * Deactivate a user (Admin only)
   */
  async deactivate(id: string): Promise<{ success: boolean; message: string }> {
    return apiClient.patch<{ success: boolean; message: string }>(`/users/${id}/deactivate`);
  },

  /**
   * Reset user password (Admin only)
   */
  async resetPassword(
    id: string,
    data: UserResetPasswordRequest
  ): Promise<UserResetPasswordResponse> {
    return apiClient.post<UserResetPasswordResponse>(`/users/${id}/reset-password`, data);
  },
};
