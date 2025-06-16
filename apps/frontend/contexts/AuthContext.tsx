"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter, usePathname } from "next/navigation";

import { authAPI } from "@/lib/api";
import {
  setTokens,
  getTokens,
  removeTokens,
  isAuthenticated,
} from "@/lib/auth";

// Define User type
interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

// Define AuthContext type
interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

interface RegisterData {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  password: string;
  password2: string;
}

// Create the AuthContext
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Protected routes - paths that require authentication
const protectedRoutes = [
  "/dashboard",
  "/journal",
  "/finance",
  "/info",
  "/settings",
];

// Public routes - paths that don't require authentication
const publicRoutes = ["/login", "/register", "/forget-password"];

// AuthProvider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  // Clear error
  const clearError = () => {
    setError(null);
  };

  // Check if the user is authenticated
  const checkAuth = async () => {
    try {
      // Skip auth check for public routes
      if (publicRoutes.includes(pathname)) {
        setLoading(false);

        return;
      }

      setLoading(true);

      if (!isAuthenticated()) {
        // If the route requires authentication, redirect to login
        if (protectedRoutes.some((route) => pathname.startsWith(route))) {
          router.push("/login");
        }
        setLoading(false);

        return;
      }

      // Get user profile
      const response = await authAPI.getProfile();

      setUser(response.data);

      // If on login page but authenticated, redirect to dashboard
      if (
        pathname === "/login" ||
        pathname === "/register" ||
        pathname === "/forget-password"
      ) {
        router.push("/dashboard");
      }
    } catch (err) {
      console.error("Auth check error:", err);

      // If auth error and on protected route, redirect to login
      if (protectedRoutes.some((route) => pathname.startsWith(route))) {
        removeTokens();
        router.push("/login");
      }
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      const response = await authAPI.login({ username, password });

      console.log("Login response:", response.data); // Debug log

      // Store tokens
      setTokens({
        access: response.data.tokens.access,
        refresh: response.data.tokens.refresh,
      });

      // Set user data
      setUser(response.data.user);

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      console.error("Login error:", err); // Debug log
      setError(err.response?.data?.error || err.message || "Login failed");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (userData: RegisterData) => {
    try {
      setLoading(true);
      setError(null);

      await authAPI.register(userData);

      // Redirect to login page
      router.push("/login?registered=true");
    } catch (err: any) {
      setError(
        err.response?.data?.error || err.message || "Registration failed",
      );
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      setLoading(true);
      const tokens = getTokens();

      if (tokens) {
        await authAPI.logout(tokens.refresh);
      }

      // Clear tokens and user
      removeTokens();
      setUser(null);

      // Redirect to login
      router.push("/login");
    } catch (err: any) {
      console.error("Logout error:", err);

      // Still remove tokens and user
      removeTokens();
      setUser(null);
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  // Check authentication on initial load and URL changes
  useEffect(() => {
    checkAuth();
  }, [pathname]);

  // Context value
  const contextValue: AuthContextType = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    clearError,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

// Hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
};
