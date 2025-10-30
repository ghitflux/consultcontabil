/**
 * Notification types and interfaces
 * Mirrors backend schemas from apps/api/app/schemas/notification.py
 */

export enum NotificationType {
  // Obligation related
  OBLIGATION_CREATED = "obligation_created",
  OBLIGATION_DUE_SOON = "obligation_due_soon",
  OBLIGATION_OVERDUE = "obligation_overdue",
  OBLIGATION_COMPLETED = "obligation_completed",
  OBLIGATION_CANCELED = "obligation_canceled",

  // Client related
  CLIENT_CREATED = "client_created",
  CLIENT_UPDATED = "client_updated",
  CLIENT_DOCUMENT_UPLOADED = "client_document_uploaded",

  // User related
  USER_MENTION = "user_mention",
  USER_ASSIGNED = "user_assigned",

  // System
  SYSTEM_ALERT = "system_alert",
  SYSTEM_MAINTENANCE = "system_maintenance",
}

export interface Notification {
  id: string;
  user_id: string;
  type: NotificationType;
  title: string;
  message: string;
  link?: string;
  metadata?: Record<string, unknown>;
  read: boolean;
  read_at?: string;
  created_at: string;
}

export interface NotificationCreate {
  user_id: string;
  type: NotificationType;
  title: string;
  message: string;
  link?: string;
  metadata?: Record<string, unknown>;
}

export interface NotificationBulkCreate {
  user_ids: string[];
  type: NotificationType;
  title: string;
  message: string;
  link?: string;
  metadata?: Record<string, unknown>;
}

export interface NotificationUpdate {
  read?: boolean;
}

export interface NotificationListResponse {
  items: Notification[];
  total: number;
  unread_count: number;
  page: number;
  size: number;
  pages: number;
}

export interface NotificationMarkAllReadResponse {
  marked_count: number;
  message: string;
}

export interface NotificationStatistics {
  total: number;
  unread: number;
  by_type: Record<NotificationType, number>;
  today_count: number;
  this_week_count: number;
}

// WebSocket Event Types
export interface WebSocketEvent<T = unknown> {
  type: string;
  data?: T;
  timestamp: string;
}

export interface WebSocketNotificationEvent extends WebSocketEvent<Notification> {
  type: "notification";
  data: Notification;
}

export interface WebSocketObligationUpdateEvent extends WebSocketEvent {
  type: "obligation_update";
  data: Record<string, unknown>; // Obligation data
}

export interface WebSocketSystemEvent extends WebSocketEvent {
  type: "system";
  data: {
    message: string;
    severity?: "info" | "warning" | "error";
  };
}

export interface WebSocketConnectedEvent extends WebSocketEvent {
  type: "connected";
  message: string;
  user_id: string;
  role: string;
}

export type WebSocketEventType =
  | WebSocketNotificationEvent
  | WebSocketObligationUpdateEvent
  | WebSocketSystemEvent
  | WebSocketConnectedEvent;

// Notification filters for API queries
export interface NotificationFilters {
  type?: NotificationType;
  read?: boolean;
  date_from?: string;
  date_to?: string;
  page?: number;
  size?: number;
}

// Helper functions
export function getNotificationIcon(type: NotificationType): string {
  switch (type) {
    case NotificationType.OBLIGATION_CREATED:
      return "📋";
    case NotificationType.OBLIGATION_DUE_SOON:
      return "⏰";
    case NotificationType.OBLIGATION_OVERDUE:
      return "🚨";
    case NotificationType.OBLIGATION_COMPLETED:
      return "✅";
    case NotificationType.OBLIGATION_CANCELED:
      return "❌";
    case NotificationType.CLIENT_CREATED:
      return "👤";
    case NotificationType.CLIENT_UPDATED:
      return "✏️";
    case NotificationType.CLIENT_DOCUMENT_UPLOADED:
      return "📄";
    case NotificationType.USER_MENTION:
      return "💬";
    case NotificationType.USER_ASSIGNED:
      return "👥";
    case NotificationType.SYSTEM_ALERT:
      return "⚠️";
    case NotificationType.SYSTEM_MAINTENANCE:
      return "🔧";
    default:
      return "🔔";
  }
}

export function getNotificationColor(
  type: NotificationType
): "default" | "primary" | "secondary" | "success" | "warning" | "danger" {
  switch (type) {
    case NotificationType.OBLIGATION_OVERDUE:
    case NotificationType.SYSTEM_ALERT:
      return "danger";

    case NotificationType.OBLIGATION_DUE_SOON:
      return "warning";

    case NotificationType.OBLIGATION_COMPLETED:
      return "success";

    case NotificationType.OBLIGATION_CREATED:
    case NotificationType.CLIENT_CREATED:
    case NotificationType.USER_ASSIGNED:
      return "primary";

    case NotificationType.CLIENT_UPDATED:
    case NotificationType.CLIENT_DOCUMENT_UPLOADED:
    case NotificationType.USER_MENTION:
      return "secondary";

    default:
      return "default";
  }
}

export function getNotificationTitle(type: NotificationType): string {
  switch (type) {
    case NotificationType.OBLIGATION_CREATED:
      return "Nova Obrigação";
    case NotificationType.OBLIGATION_DUE_SOON:
      return "Obrigação Próxima ao Vencimento";
    case NotificationType.OBLIGATION_OVERDUE:
      return "Obrigação Atrasada";
    case NotificationType.OBLIGATION_COMPLETED:
      return "Obrigação Concluída";
    case NotificationType.OBLIGATION_CANCELED:
      return "Obrigação Cancelada";
    case NotificationType.CLIENT_CREATED:
      return "Novo Cliente";
    case NotificationType.CLIENT_UPDATED:
      return "Cliente Atualizado";
    case NotificationType.CLIENT_DOCUMENT_UPLOADED:
      return "Documento Enviado";
    case NotificationType.USER_MENTION:
      return "Você foi Mencionado";
    case NotificationType.USER_ASSIGNED:
      return "Nova Atribuição";
    case NotificationType.SYSTEM_ALERT:
      return "Alerta do Sistema";
    case NotificationType.SYSTEM_MAINTENANCE:
      return "Manutenção Programada";
    default:
      return "Notificação";
  }
}

// Type guard for WebSocket events
export function isNotificationEvent(
  event: WebSocketEvent
): event is WebSocketNotificationEvent {
  return event.type === "notification";
}

export function isObligationUpdateEvent(
  event: WebSocketEvent
): event is WebSocketObligationUpdateEvent {
  return event.type === "obligation_update";
}

export function isSystemEvent(event: WebSocketEvent): event is WebSocketSystemEvent {
  return event.type === "system";
}

export function isConnectedEvent(
  event: WebSocketEvent
): event is WebSocketConnectedEvent {
  return event.type === "connected";
}
