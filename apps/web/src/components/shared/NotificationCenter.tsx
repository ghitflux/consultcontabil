"use client";

import {
  Badge,
  Button,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  DropdownSection,
  Chip,
} from "@/heroui";
import { useNotifications, Notification } from "@/hooks/websocket/useNotifications";
import { BellIcon } from "@/lib/icons";
import { useState } from "react";

export function NotificationCenter() {
  const {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearNotification,
    clearAll,
  } = useNotifications();

  const [isOpen, setIsOpen] = useState(false);

  const getNotificationColor = (type: string) => {
    switch (type) {
      case "danger":
        return "danger";
      case "warning":
        return "warning";
      case "success":
        return "success";
      case "obligation":
        return "primary";
      default:
        return "default";
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case "danger":
        return "🚨";
      case "warning":
        return "⚠️";
      case "success":
        return "✅";
      case "obligation":
        return "📋";
      default:
        return "🔔";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Agora";
    if (diffMins < 60) return `${diffMins}m atrás`;
    if (diffHours < 24) return `${diffHours}h atrás`;
    if (diffDays < 7) return `${diffDays}d atrás`;

    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "short",
    }).format(date);
  };

  const handleNotificationClick = (notification: Notification) => {
    if (!notification.read) {
      markAsRead(notification.id);
    }
    setIsOpen(false);

    // Navigate to relevant page based on notification data
    if (notification.data?.obligation_id) {
      window.location.href = `/obrigacoes?id=${notification.data.obligation_id}`;
    }
  };

  return (
    <Dropdown isOpen={isOpen} onOpenChange={setIsOpen} placement="bottom-end">
      <DropdownTrigger>
        <Button
          isIconOnly
          variant="light"
          className="relative"
          aria-label="Notificações"
        >
          {unreadCount > 0 ? (
            <Badge content={unreadCount} color="danger" size="sm">
              <BellIcon className="h-5 w-5" />
            </Badge>
          ) : (
            <BellIcon className="h-5 w-5" />
          )}
        </Button>
      </DropdownTrigger>

      <DropdownMenu
        aria-label="Notificações"
        className="w-80 max-h-96 overflow-y-auto"
        classNames={{
          base: "p-0",
          list: "p-0",
        }}
      >
        {/* Header */}
        <DropdownSection showDivider>
          <DropdownItem
            key="header"
            isReadOnly
            className="cursor-default hover:bg-transparent"
            textValue="Header"
          >
            <div className="flex justify-between items-center px-2 py-2">
              <h3 className="text-lg font-semibold">Notificações</h3>
              {notifications.length > 0 && (
                <div className="flex gap-2">
                  {unreadCount > 0 && (
                    <Button
                      size="sm"
                      variant="light"
                      onPress={markAllAsRead}
                    >
                      Marcar todas como lidas
                    </Button>
                  )}
                  <Button
                    size="sm"
                    variant="light"
                    color="danger"
                    onPress={clearAll}
                  >
                    Limpar
                  </Button>
                </div>
              )}
            </div>
          </DropdownItem>
        </DropdownSection>

        {/* Notifications list */}
        {notifications.length === 0 ? (
          <DropdownItem
            key="empty"
            isReadOnly
            className="cursor-default hover:bg-transparent"
            textValue="Nenhuma notificação"
          >
            <div className="text-center py-8 text-default-400">
              <p className="text-4xl mb-2">📭</p>
              <p>Nenhuma notificação</p>
            </div>
          </DropdownItem>
        ) : (
          <>
            {notifications.map((notification) => (
              <DropdownItem
                key={notification.id}
                textValue={notification.title}
                className={`cursor-pointer ${
                  !notification.read ? "bg-primary-50/50" : ""
                }`}
                onPress={() => handleNotificationClick(notification)}
              >
                <div className="flex gap-3 py-2">
                  {/* Icon */}
                  <div className="flex-shrink-0 text-2xl">
                    {getNotificationIcon(notification.type)}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="font-semibold text-sm truncate">
                        {notification.title}
                      </p>
                      {!notification.read && (
                        <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
                      )}
                    </div>
                    <p className="text-xs text-default-500 line-clamp-2">
                      {notification.message}
                    </p>
                    <div className="flex items-center gap-2 mt-1">
                      <Chip
                        size="sm"
                        color={getNotificationColor(notification.type) as any}
                        variant="flat"
                        classNames={{
                          base: "h-5",
                          content: "text-xs",
                        }}
                      >
                        {notification.type}
                      </Chip>
                      <span className="text-xs text-default-400">
                        {formatDate(notification.created_at)}
                      </span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex-shrink-0">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      onPress={() => {
                        clearNotification(notification.id);
                      }}
                      aria-label="Remover notificação"
                    >
                      ✕
                    </Button>
                  </div>
                </div>
              </DropdownItem>
            ))}
          </>
        )}
      </DropdownMenu>
    </Dropdown>
  );
}
