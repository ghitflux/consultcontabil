"use client";

import { Card, CardBody, CardHeader, Chip, Divider, Spinner } from "@/heroui";
import { useEffect, useState } from "react";

export interface ObligationEvent {
  id: string;
  obligation_id: string;
  event_type: string;
  description: string;
  performed_by_id?: string;
  performed_by_name?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

interface ObligationTimelineProps {
  obligationId: string;
}

export function ObligationTimeline({ obligationId }: ObligationTimelineProps) {
  const [events, setEvents] = useState<ObligationEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEvents();
  }, [obligationId]);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations/${obligationId}/events`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch events");
      }

      const data = await response.json();
      setEvents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case "CREATED":
        return "📝";
      case "STATUS_CHANGED":
        return "🔄";
      case "RECEIPT_UPLOADED":
        return "📎";
      case "DUE_DATE_CHANGED":
        return "📅";
      case "CANCELLED":
        return "❌";
      case "COMMENT_ADDED":
        return "💬";
      default:
        return "•";
    }
  };

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case "CREATED":
        return "default";
      case "STATUS_CHANGED":
        return "primary";
      case "RECEIPT_UPLOADED":
        return "success";
      case "DUE_DATE_CHANGED":
        return "warning";
      case "CANCELLED":
        return "danger";
      case "COMMENT_ADDED":
        return "secondary";
      default:
        return "default";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <CardBody>
          <p className="text-danger">{error}</p>
        </CardBody>
      </Card>
    );
  }

  if (events.length === 0) {
    return (
      <Card>
        <CardBody>
          <p className="text-default-500">Nenhum evento registrado.</p>
        </CardBody>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold">Histórico de Eventos</h3>
      </CardHeader>
      <Divider />
      <CardBody>
        <div className="relative">
          {/* Timeline line */}
          <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-default-200" />

          {/* Events */}
          <div className="space-y-6">
            {events.map((event) => (
              <div key={event.id} className="relative pl-12">
                {/* Event icon */}
                <div className="absolute left-0 w-8 h-8 rounded-full bg-default-100 flex items-center justify-center text-lg">
                  {getEventIcon(event.event_type)}
                </div>

                {/* Event content */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Chip
                      size="sm"
                      color={getEventColor(event.event_type) as any}
                      variant="flat"
                    >
                      {event.event_type.replace(/_/g, " ")}
                    </Chip>
                    <span className="text-sm text-default-500">
                      {formatDate(event.created_at)}
                    </span>
                  </div>

                  <p className="text-sm">{event.description}</p>

                  {event.performed_by_name && (
                    <p className="text-xs text-default-400">
                      Por: {event.performed_by_name}
                    </p>
                  )}

                  {event.metadata && Object.keys(event.metadata).length > 0 && (
                    <details className="text-xs text-default-400 cursor-pointer">
                      <summary className="hover:text-default-600">
                        Ver detalhes
                      </summary>
                      <pre className="mt-2 p-2 bg-default-100 rounded text-xs overflow-auto">
                        {JSON.stringify(event.metadata, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardBody>
    </Card>
  );
}
