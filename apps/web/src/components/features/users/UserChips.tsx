/**
 * User role and status chips components
 */

import { Chip } from "@heroui/react";
import { getRoleColor, getRoleLabel, getStatusColor, getStatusLabel, type UserRole } from "@/types/user";

interface UserRoleChipProps {
  role: UserRole;
  size?: "sm" | "md" | "lg";
}

export function UserRoleChip({ role, size = "sm" }: UserRoleChipProps) {
  return (
    <Chip color={getRoleColor(role)} size={size} variant="flat">
      {getRoleLabel(role)}
    </Chip>
  );
}

interface UserStatusChipProps {
  isActive: boolean;
  size?: "sm" | "md" | "lg";
}

export function UserStatusChip({ isActive, size = "sm" }: UserStatusChipProps) {
  return (
    <Chip color={getStatusColor(isActive)} size={size} variant="flat">
      {getStatusLabel(isActive)}
    </Chip>
  );
}
