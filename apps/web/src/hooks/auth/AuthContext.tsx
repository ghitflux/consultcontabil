"use client";

/**
 * Authentication context and provider.
 */

import type { AuthContextValue, AuthState } from "@/types/auth";
import type { User } from "@/types/user";

import { authApi } from "@/lib/api/endpoints/auth";
import React, { createContext, useCallback, useEffect, useState } from "react";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Initialize auth state from storage
  useEffect(() => {
    const initAuth = async () => {
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          // Try to get current user
          const user = await authApi.me();
          setState((prev) => ({
            ...prev,
            user,
            refreshToken,
            isAuthenticated: true,
            isLoading: false,
          }));
        } else {
          setState((prev) => ({ ...prev, isLoading: false }));
        }
      } catch (error) {
        // Refresh token is invalid or expired
        localStorage.removeItem("refresh_token");
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    };

    initAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await authApi.login({ email, password });

      setState({
        user: response.user,
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Login failed";

      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      throw error;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } finally {
      setState({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  }, []);

  const refresh = useCallback(async () => {
    const refreshToken = state.refreshToken || localStorage.getItem("refresh_token");

    if (!refreshToken) {
      throw new Error("No refresh token available");
    }

    try {
      const response = await authApi.refresh(refreshToken);

      setState((prev) => ({
        ...prev,
        accessToken: response.access_token,
      }));
    } catch (error) {
      // Refresh failed, logout
      await logout();
      throw error;
    }
  }, [state.refreshToken, logout]);

  const updateUser = useCallback((user: User) => {
    setState((prev) => ({
      ...prev,
      user,
    }));
  }, []);

  const value: AuthContextValue = {
    ...state,
    login,
    logout,
    refresh,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = React.useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
