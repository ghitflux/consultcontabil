"use client";

import { useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Checkbox,
  Card,
  CardBody,
} from "@heroui/react";
import { CopyIcon, CheckIcon, KeyIcon } from "@/lib/icons";
import { useUsers } from "@/hooks/useUsers";
import type { UserListItem } from "@/types/user";

interface ResetPasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: UserListItem | null;
}

export function ResetPasswordModal({ isOpen, onClose, user }: ResetPasswordModalProps) {
  const { resetPassword, isLoading } = useUsers();

  // Form state
  const [generateTemporary, setGenerateTemporary] = useState(true);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Result state
  const [temporaryPassword, setTemporaryPassword] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle submit
  const handleSubmit = async () => {
    if (!user) return;

    setError(null);

    // Validation for manual password
    if (!generateTemporary) {
      if (!newPassword || newPassword.length < 8) {
        setError("Senha deve ter no mínimo 8 caracteres");
        return;
      }
      if (!/[a-zA-Z]/.test(newPassword) || !/\d/.test(newPassword)) {
        setError("Senha deve conter letras e números");
        return;
      }
      if (newPassword !== confirmPassword) {
        setError("As senhas não coincidem");
        return;
      }
    }

    try {
      const response = await resetPassword(user.id, {
        generate_temporary: generateTemporary,
        new_password: generateTemporary ? undefined : newPassword,
      });

      if (response.temporary_password) {
        setTemporaryPassword(response.temporary_password);
      } else {
        // Success without temp password (manual password set)
        onClose();
        resetForm();
      }
    } catch (err: any) {
      setError(err.message || "Erro ao resetar senha");
    }
  };

  // Handle copy
  const handleCopy = () => {
    if (temporaryPassword) {
      navigator.clipboard.writeText(temporaryPassword);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Handle close
  const handleClose = () => {
    resetForm();
    onClose();
  };

  const resetForm = () => {
    setGenerateTemporary(true);
    setNewPassword("");
    setConfirmPassword("");
    setTemporaryPassword(null);
    setCopied(false);
    setError(null);
  };

  // If showing temporary password
  if (temporaryPassword) {
    return (
      <Modal isOpen={isOpen} onClose={handleClose} size="md" placement="center">
        <ModalContent>
          <ModalHeader className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <KeyIcon className="h-5 w-5 text-success" />
              <span>Senha Resetada com Sucesso!</span>
            </div>
          </ModalHeader>
          <ModalBody>
            <div className="space-y-4">
              <p className="text-sm text-default-600">
                Uma senha temporária foi gerada para <strong>{user?.name}</strong>:
              </p>

              <Card className="bg-success-50">
                <CardBody>
                  <div className="flex items-center justify-between gap-3">
                    <code className="text-lg font-mono font-semibold text-success-700">
                      {temporaryPassword}
                    </code>
                    <Button
                      isIconOnly
                      size="sm"
                      color={copied ? "success" : "default"}
                      variant="flat"
                      onPress={handleCopy}
                      aria-label="Copiar senha"
                    >
                      {copied ? <CheckIcon className="h-4 w-4" /> : <CopyIcon className="h-4 w-4" />}
                    </Button>
                  </div>
                </CardBody>
              </Card>

              <div className="rounded-lg bg-warning-50 p-3">
                <p className="text-sm text-warning-700">
                  <strong>⚠️ Atenção:</strong> Copie esta senha antes de fechar esta janela. O usuário
                  deverá alterar a senha no primeiro acesso.
                </p>
              </div>
            </div>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onPress={handleClose}>
              Fechar
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    );
  }

  // Form view
  return (
    <Modal isOpen={isOpen} onClose={handleClose} size="lg" placement="center">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">
          Resetar Senha
        </ModalHeader>
        <ModalBody>
          <div className="space-y-4">
            <p className="text-sm text-default-600">
              Resetar senha para: <strong>{user?.name}</strong> ({user?.email})
            </p>

            {error && (
              <div className="rounded-lg bg-danger-50 p-3 text-sm text-danger">
                {error}
              </div>
            )}

            {/* Option: Generate temporary */}
            <Checkbox
              isSelected={generateTemporary}
              onValueChange={setGenerateTemporary}
            >
              <span className="text-sm">
                Gerar senha temporária automaticamente (recomendado)
              </span>
            </Checkbox>

            {/* Manual password fields */}
            {!generateTemporary && (
              <div className="space-y-3 pl-6">
                <Input
                  label="Nova senha"
                  placeholder="Mínimo 8 caracteres"
                  type="password"
                  value={newPassword}
                  onValueChange={setNewPassword}
                  description="Deve conter letras e números"
                />

                <Input
                  label="Confirmar senha"
                  placeholder="Digite a senha novamente"
                  type="password"
                  value={confirmPassword}
                  onValueChange={setConfirmPassword}
                />
              </div>
            )}

            {/* Info box */}
            <div className="rounded-lg bg-default-100 p-3 text-sm text-default-600">
              {generateTemporary ? (
                <>
                  💡 Uma senha temporária segura será gerada automaticamente. O usuário
                  receberá a senha e deverá alterá-la no próximo acesso.
                </>
              ) : (
                <>
                  💡 Você está definindo uma nova senha manualmente. Certifique-se de
                  comunicá-la ao usuário de forma segura.
                </>
              )}
            </div>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button variant="light" onPress={handleClose} isDisabled={isLoading}>
            Cancelar
          </Button>
          <Button color="primary" onPress={handleSubmit} isLoading={isLoading}>
            Resetar Senha
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
