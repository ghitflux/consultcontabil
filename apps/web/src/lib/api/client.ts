/**
 * API client with authentication and refresh token interceptors.
 */

import type { RefreshResponse } from "@/types/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Queue for requests waiting for token refresh
let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];

function onRefreshed(token: string) {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
}

function addRefreshSubscriber(callback: (token: string) => void) {
  refreshSubscribers.push(callback);
}

export interface ApiError extends Error {
  status?: number;
  data?: any;
}

export class ApiClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor() {
    // Load tokens from localStorage on init
    if (typeof window !== "undefined") {
      this.accessToken = localStorage.getItem("access_token");
      this.refreshToken = localStorage.getItem("refresh_token");
    }
  }

  setTokens(accessToken: string, refreshToken: string) {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    if (typeof window !== "undefined") {
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);
    }
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }

  private async refreshAccessToken(): Promise<string> {
    if (!this.refreshToken) {
      throw new Error("No refresh token available");
    }

    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh_token: this.refreshToken }),
    });

    if (!response.ok) {
      this.clearTokens();
      throw new Error("Failed to refresh token");
    }

    const data: RefreshResponse = await response.json();
    this.accessToken = data.access_token;
    return data.access_token;
  }

  async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    // Add Authorization header if token is available
    const headers = new Headers(options.headers);
    // Try to get token from localStorage if not already set
    if (!this.accessToken && typeof window !== "undefined") {
      this.accessToken = localStorage.getItem("access_token");
    }
    if (this.accessToken && !headers.has("Authorization")) {
      headers.set("Authorization", `Bearer ${this.accessToken}`);
    }
    if (!headers.has("Content-Type") && options.body) {
      headers.set("Content-Type", "application/json");
    }

    const config: RequestInit = {
      ...options,
      headers,
    };

    let response = await fetch(url, config);

    // Handle 401 - Try to refresh token
    if (response.status === 401 && this.refreshToken) {
      if (isRefreshing) {
        // Wait for ongoing refresh to complete
        return new Promise((resolve, reject) => {
          addRefreshSubscriber(async (token: string) => {
            try {
              headers.set("Authorization", `Bearer ${token}`);
              const retryResponse = await fetch(url, { ...config, headers });
              if (retryResponse.ok) {
                resolve(await retryResponse.json());
              } else {
                reject(new Error("Retry request failed"));
              }
            } catch (error) {
              reject(error);
            }
          });
        });
      }

      isRefreshing = true;

      try {
        const newToken = await this.refreshAccessToken();
        isRefreshing = false;
        onRefreshed(newToken);

        // Save new token to localStorage
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", newToken);
        }

        // Retry original request with new token
        headers.set("Authorization", `Bearer ${newToken}`);
        response = await fetch(url, { ...config, headers });
      } catch (error) {
        isRefreshing = false;
        this.clearTokens();
        throw error;
      }
    }

    // Handle non-OK responses
    if (!response.ok) {
      const error: ApiError = new Error(`API Error: ${response.statusText}`);
      error.status = response.status;
      try {
        error.data = await response.json();
      } catch {
        // Response is not JSON
      }
      throw error;
    }

    // Return JSON response
    try {
      return await response.json();
    } catch {
      // Response is not JSON (e.g., 204 No Content)
      return undefined as T;
    }
  }

  async get<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  async post<T = any>(
    endpoint: string,
    data?: any,
    options: RequestInit = {}
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T = any>(
    endpoint: string,
    data?: any,
    options: RequestInit = {}
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
