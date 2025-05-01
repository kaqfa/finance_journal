// Auth utility functions

import axios from 'axios';

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
  if (typeof window !== 'undefined') {
    localStorage.setItem('accessToken', tokens.access);
    localStorage.setItem('refreshToken', tokens.refresh);
  }
};

// Get stored tokens
export const getTokens = (): Tokens | null => {
  if (typeof window !== 'undefined') {
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    
    if (access && refresh) {
      return { access, refresh };
    }
  }
  return null;
};

// Remove stored tokens
export const removeTokens = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
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

    const response = await axios.get('/api/v1/auth/profile/', {
      headers: {
        Authorization: `Bearer ${tokens.access}`,
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }
};

// Refresh the access token using refresh token
export const refreshAccessToken = async (): Promise<string | null> => {
  try {
    const tokens = getTokens();
    if (!tokens) return null;

    const response = await axios.post('/api/v1/auth/token/refresh/', {
      refresh: tokens.refresh,
    });

    const newAccessToken = response.data.access;
    setTokens({ access: newAccessToken, refresh: tokens.refresh });
    
    return newAccessToken;
  } catch (error) {
    console.error('Error refreshing token:', error);
    removeTokens();
    return null;
  }
};

// Logout function
export const logout = async (): Promise<boolean> => {
  try {
    const tokens = getTokens();
    if (!tokens) return true;

    await axios.post('/api/v1/auth/logout/', {
      refresh: tokens.refresh,
    }, {
      headers: {
        Authorization: `Bearer ${tokens.access}`,
      },
    });

    removeTokens();
    return true;
  } catch (error) {
    console.error('Error during logout:', error);
    // Still remove tokens even if API call fails
    removeTokens();
    return false;
  }
};

// Create axios instance with authentication
export const createAuthenticatedAxios = () => {
  const instance = axios.create({
    baseURL: '/api',
  });

  // Add auth token to requests
  instance.interceptors.request.use(
    async (config) => {
      const tokens = getTokens();
      if (tokens) {
        config.headers.Authorization = `Bearer ${tokens.access}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Handle token refresh on 401 errors
  instance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      
      // If error is 401 and we haven't already tried to refresh
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        const newToken = await refreshAccessToken();
        
        if (newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return instance(originalRequest);
        }
      }
      
      return Promise.reject(error);
    }
  );

  return instance;
};

// Create a default authenticated axios instance
export const api = createAuthenticatedAxios();