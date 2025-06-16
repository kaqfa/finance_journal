// Auth utility functions

import { authAPI } from "./api";

interface Tokens {
  access: string;
  refresh: string;
}

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

// Store auth tokens
export const setTokens = (tokens: Tokens): void => {
  if (typeof window !== "undefined") {
    localStorage.setItem("accessToken", tokens.access);
    localStorage.setItem("refreshToken", tokens.refresh);
  }
};

// Get stored tokens
export const getTokens = (): Tokens | null => {
  if (typeof window !== "undefined") {
    const access = localStorage.getItem("accessToken");
    const refresh = localStorage.getItem("refreshToken");

    if (access && refresh) {
      return { access, refresh };
    }
  }

  return null;
};

// Remove stored tokens
export const removeTokens = (): void => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
  }
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return getTokens() !== null;
};

// Get the current user's profile
export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const tokens = getTokens();

    if (!tokens) return null;

    const response = await authAPI.getProfile();

    return response.data;
  } catch (error) {
    console.error("Error fetching user profile:", error);

    return null;
  }
};

// Logout function
export const logout = async (): Promise<boolean> => {
  try {
    const tokens = getTokens();

    if (!tokens) return true;

    await authAPI.logout(tokens.refresh);
    removeTokens();

    return true;
  } catch (error) {
    console.error("Error during logout:", error);
    removeTokens();

    return false;
  }
};

// Refresh the access token using refresh token
export const refreshAccessToken = async (): Promise<string | null> => {
  try {
    const tokens = getTokens();

    if (!tokens) return null;

    const response = await authAPI.refreshToken(tokens.refresh);
    const newAccessToken = response.data.access;

    setTokens({ access: newAccessToken, refresh: tokens.refresh });

    return newAccessToken;
  } catch (error) {
    console.error("Error refreshing token:", error);
    removeTokens();

    return null;
  }
};
