/**
 * User types and interfaces.
 */

export enum UserRole {
  ADMIN = "admin",
  FUNC = "func",
  CLIENTE = "cliente",
}

export interface UserBase {
  name: string;
  email: string;
  role: UserRole;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
  role?: UserRole;
  is_active?: boolean;
  is_verified?: boolean;
}

export interface UserUpdatePassword {
  current_password: string;
  new_password: string;
}

export interface User extends UserBase {
  id: string;
  is_active: boolean;
  is_verified: boolean;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserInDB extends User {
  password_hash: string;
}

/**
 * Type guard to check if user has a specific role.
 */
export function hasRole(user: User | null, roles: UserRole[]): boolean {
  return user !== null && roles.includes(user.role);
}

/**
 * Type guard to check if user is admin.
 */
export function isAdmin(user: User | null): boolean {
  return hasRole(user, [UserRole.ADMIN]);
}

/**
 * Type guard to check if user is funcionario.
 */
export function isFuncionario(user: User | null): boolean {
  return hasRole(user, [UserRole.FUNC]);
}

/**
 * Type guard to check if user is cliente.
 */
export function isCliente(user: User | null): boolean {
  return hasRole(user, [UserRole.CLIENTE]);
}

// Additional types for user management

export interface UserListItem extends User {}

export interface UserResetPasswordRequest {
  generate_temporary?: boolean;
  new_password?: string;
}

export interface UserResetPasswordResponse {
  success: boolean;
  temporary_password?: string;
  message: string;
}

export interface PaginatedUsersResponse {
  items: UserListItem[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface LinkUserToClientRequest {
  user_id: string;
  access_level: "OWNER" | "MANAGER" | "VIEWER";
}

// Helper functions
export const getRoleLabel = (role: UserRole): string => {
  const labels: Record<UserRole, string> = {
    [UserRole.ADMIN]: "Administrador",
    [UserRole.FUNC]: "Funcionário",
    [UserRole.CLIENTE]: "Cliente",
  };
  return labels[role];
};

export const getRoleColor = (role: UserRole): "danger" | "primary" | "secondary" => {
  const colors: Record<UserRole, "danger" | "primary" | "secondary"> = {
    [UserRole.ADMIN]: "danger",
    [UserRole.FUNC]: "primary",
    [UserRole.CLIENTE]: "secondary",
  };
  return colors[role];
};

export const getStatusLabel = (is_active: boolean): string => {
  return is_active ? "Ativo" : "Inativo";
};

export const getStatusColor = (is_active: boolean): "success" | "default" => {
  return is_active ? "success" : "default";
};
