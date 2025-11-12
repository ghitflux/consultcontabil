"use client";

import { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Select,
  SelectItem,
} from "@heroui/react";
import { useUsers } from "@/hooks/useUsers";
import type { UserListItem, UserRole } from "@/types/user";
import { getRoleLabel } from "@/types/user";

interface UserFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  user?: UserListItem | null;
}

export function UserFormModal({ isOpen, onClose, user }: UserFormModalProps) {
  const { createUser, updateUser, isLoading } = useUsers();

  // Form state
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<UserRole>("func");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Error state
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Is editing?
  const isEditing = Boolean(user);

  // Initialize form with user data
  useEffect(() => {
    if (user) {
      setName(user.name);
      setEmail(user.email);
      setRole(user.role);
      // Password fields remain empty for editing
      setPassword("");
      setConfirmPassword("");
    } else {
      // Reset form for new user
      setName("");
      setEmail("");
      setRole("func");
      setPassword("");
      setConfirmPassword("");
    }
    setErrors({});
  }, [user, isOpen]);

  // Validation
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Name
    if (!name.trim()) {
      newErrors.name = "Nome é obrigatório";
    }

    // Email
    if (!email.trim()) {
      newErrors.email = "Email é obrigatório";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Email inválido";
    }

    // Password (only for create)
    if (!isEditing) {
      if (!password) {
        newErrors.password = "Senha é obrigatória";
      } else if (password.length < 8) {
        newErrors.password = "Senha deve ter no mínimo 8 caracteres";
      } else if (!/[a-zA-Z]/.test(password)) {
        newErrors.password = "Senha deve conter pelo menos uma letra";
      } else if (!/\d/.test(password)) {
        newErrors.password = "Senha deve conter pelo menos um número";
      }

      if (!confirmPassword) {
        newErrors.confirmPassword = "Confirme a senha";
      } else if (password !== confirmPassword) {
        newErrors.confirmPassword = "As senhas não coincidem";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle submit
  const handleSubmit = async () => {
    if (!validate()) return;

    try {
      if (isEditing && user) {
        // Update existing user
        await updateUser(user.id, {
          name,
          email,
          role,
        });
      } else {
        // Create new user
        await createUser({
          name,
          email,
          role,
          password,
        });
      }

      onClose();
    } catch (error: any) {
      // Handle API errors
      if (error.message?.includes("Email")) {
        setErrors({ email: "Email já está em uso" });
      } else {
        setErrors({ general: error.message || "Erro ao salvar usuário" });
      }
    }
  };

  const handleClose = () => {
    setErrors({});
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} size="lg" placement="center">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">
          {isEditing ? "Editar Usuário" : "Novo Usuário"}
        </ModalHeader>
        <ModalBody>
          {/* General error */}
          {errors.general && (
            <div className="rounded-lg bg-danger-50 p-3 text-sm text-danger">
              {errors.general}
            </div>
          )}

          <div className="flex flex-col gap-4">
            {/* Name */}
            <Input
              label="Nome completo"
              placeholder="Digite o nome completo"
              value={name}
              onValueChange={setName}
              isRequired
              isInvalid={!!errors.name}
              errorMessage={errors.name}
              autoFocus
            />

            {/* Email */}
            <Input
              label="Email"
              placeholder="email@exemplo.com"
              type="email"
              value={email}
              onValueChange={setEmail}
              isRequired
              isInvalid={!!errors.email}
              errorMessage={errors.email}
            />

            {/* Role */}
            <Select
              label="Perfil"
              placeholder="Selecione o perfil"
              selectedKeys={[role]}
              onChange={(e) => setRole(e.target.value as UserRole)}
              isRequired
            >
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

            {/* Password (only for create) */}
            {!isEditing && (
              <>
                <Input
                  label="Senha"
                  placeholder="Mínimo 8 caracteres"
                  type="password"
                  value={password}
                  onValueChange={setPassword}
                  isRequired
                  isInvalid={!!errors.password}
                  errorMessage={errors.password}
                  description="Deve conter letras e números"
                />

                <Input
                  label="Confirmar senha"
                  placeholder="Digite a senha novamente"
                  type="password"
                  value={confirmPassword}
                  onValueChange={setConfirmPassword}
                  isRequired
                  isInvalid={!!errors.confirmPassword}
                  errorMessage={errors.confirmPassword}
                />
              </>
            )}

            {/* Info for editing */}
            {isEditing && (
              <div className="rounded-lg bg-default-100 p-3 text-sm text-default-600">
                💡 Para alterar a senha, use a opção "Resetar Senha" na tabela de usuários.
              </div>
            )}
          </div>
        </ModalBody>
        <ModalFooter>
          <Button variant="light" onPress={handleClose} isDisabled={isLoading}>
            Cancelar
          </Button>
          <Button color="primary" onPress={handleSubmit} isLoading={isLoading}>
            {isEditing ? "Salvar Alterações" : "Criar Usuário"}
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
